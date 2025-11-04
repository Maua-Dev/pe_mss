from src.modules.export_users.app.export_users_extractor import DownloadUsersExtractor
import pandas as pd
import io
import base64


class DownloadUsersTransformer:
    def __init__(self, extractor: DownloadUsersExtractor):
        self.extractor= extractor

    def __call__(self):
        users_dict= self.extractor()

        df_users= pd.DataFrame.from_dict(users_dict, orient='index')

        df_users_from_dev= df_users[df_users['organization']=='DEV']

        df_users_from_esports= df_users[df_users['organization']=='ESPORTS']

        df_users_from_metaverso= df_users[df_users['organization']=='METAVERSO']

        df_users_from_guardian= df_users[df_users['organization']=='GUARDIAN']

        df_users_from_nawat= df_users[df_users['organization']=='NAWAT']

        # para testes do dataframe
        print(df_users_from_dev.shape)
        print(df_users_from_esports.shape)
        print(df_users_from_metaverso.shape)
        print(df_users_from_guardian.shape)
        print(df_users_from_nawat.shape)

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_users_from_dev.to_excel(writer, sheet_name='DEV', index=False)
            df_users_from_esports.to_excel(writer, sheet_name='ESPORTS', index=False)
            df_users_from_metaverso.to_excel(writer, sheet_name='METAVERSO', index=False)
            df_users_from_guardian.to_excel(writer, sheet_name='GUARDIAN', index=False)
            df_users_from_nawat.to_excel(writer, sheet_name='NAWAT', index=False)

        output.seek(0)

        output_base64= base64.b64encode(output.getvalue()).decode('utf-8')

        return output_base64



