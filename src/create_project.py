import argilla as rg
import os
import json
import pandas as pd
import argparse
import art

class ArgillaProject:

    def __init__(self, workspace_name: str):

        rg.init(
            api_url=os.getenv("ARGILLA_SERVER_API_URL"), # "http://localhost:6900",
            api_key=os.getenv("ARGILLA_OWNER_API_KEY") # "argilla.apikey"
        )

        # Create workspace for project
        self.workspace = rg.Workspace.from_name(workspace_name)

    def add_users(self):
        # Create users
        # role must be one of "owner", "admin", "annotator", but only add annotator
        with open('../config/users.json', 'r') as user_file:
            users = [line for line in user_file.readlines()]

        for user in users:
            user = rg.User.create(
                username = user["new-user"],
                first_name = user["first_name"],
                last_name = user["last_name"],
                password=user["password"],
                role=user["role"],
                workspaces=[self.workspace_name]
            )

    def add_dataset(self, dataset: str):

        # Text Classification
        with open('../config/dataset.json', 'r') as dataset_file:
            dataset_configs = json.loads(dataset_file.read())
            work_dataset = dataset_configs[dataset]

        settings = rg.TextClassificationSettings(
            label_schema=work_dataset['labels']
        )

        rg.configure_dataset_settings(
            workspace=self.workspace_name,
            name=work_dataset['dataset_name'],
            settings=settings
        )


        data = pd.read_csv(work_dataset['dataset_path'])
        data = data.reset_index()
        for index, row in data.iterrows():
            rec = rg.TextClassificationRecord(
                text=row['text'],
                # prediction=[("price", 0.75), ("hygiene", 0.25)],
                # annotation="price" # row['label'] for pre-chosen labels
            )
            rg.log(
                records=rec,
                name=work_dataset['dataset_name']
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Initialize a workspace on Argilla server with users and dataset"
    )
    parser.add_argument("-wn", "--workspacename", type=str)
    parser.add_argument("-dt", "--dataset", type=str)
    args = parser.parse()

    ap = ArgillaProject(workspace_name=args.workspacename)
    ap.add_dataset(args.dataset)
    art.tprint("READY TO ANNOTATE!")
