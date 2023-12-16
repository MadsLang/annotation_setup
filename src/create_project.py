import argilla as rg
import os
import json
import pandas as pd
import argparse
import art
from ast import literal_eval
from tqdm import tqdm

class ArgillaProject:

    def __init__(self, workspace_name: str):

        api_url = os.getenv("ARGILLA_SERVER_API_URL") # "http://localhost:6900",
        api_key = os.getenv("ARGILLA_OWNER_API_KEY") # "argilla.apikey"
        print(f"Connect to Argilla at {api_url} with key: {api_key}")
        rg.init(
            api_url=api_url,
            api_key=api_key,
        )

        # Create workspace for project
        try:
            self.workspace = rg.Workspace.create(workspace_name)
        except ValueError:
            self.workspace = rg.Workspace.from_name(workspace_name)

        print(f"... Working on workspace: {self.workspace.name}")


    def add_users(self):
        print("... Adding users")
        # Create users
        # role must be one of "owner", "admin", "annotator", but only add annotator
        with open('config/users.jsonl', 'r') as user_file:
            users = [literal_eval(line) for line in user_file.readlines()]

        for user in users:
            try:
                user = rg.User.create(
                    username = user["username"],
                    first_name = user["first_name"],
                    last_name = user["last_name"],
                    password=user["password"],
                    role=user["role"],
                    workspaces=[self.workspace.name]
                )
            except KeyError:
                Warning("User already exists!")

    def add_dataset(self, dataset: str):

        # Text Classification
        with open('config/dataset.json', 'r') as dataset_file:
            dataset_configs = json.loads(dataset_file.read())
            work_dataset = dataset_configs[dataset]

        print(f"... Adding dataset {work_dataset['dataset_name']} to {self.workspace.name}")

        print("... Adding records to dataset")
        data = pd.read_csv(work_dataset['dataset_path'])
        data = data.reset_index()

        records = [
            rg.TextClassificationRecord(
                text=row['text'],
                # prediction=[("price", 0.75), ("hygiene", 0.25)],
                # annotation="price" # row['label'] for pre-chosen labels
            ) for idx, row in tqdm(data.iterrows())
        ]
        ag_dataset = rg.DatasetForTextClassification(records)

        rg.log(
            records=ag_dataset,
            name=work_dataset['dataset_name']
        )

        settings = rg.TextClassificationSettings(
            label_schema=work_dataset['labels']
        )
        rg.configure_dataset_settings(
            workspace=self.workspace.name,
            name=work_dataset['dataset_name'],
            settings=settings
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Initialize a workspace on Argilla server with users and dataset"
    )
    parser.add_argument("-wn", "--workspacename", type=str)
    parser.add_argument("-dt", "--dataset", type=str)
    args = parser.parse_args()

    ap = ArgillaProject(workspace_name=args.workspacename)
    ap.add_users()
    ap.add_dataset(args.dataset)
    art.tprint("READY TO ANNOTATE!")
