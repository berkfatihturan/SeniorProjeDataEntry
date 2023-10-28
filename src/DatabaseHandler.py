import pandas as pd
import json


def json_to_excel(json_data, excel_file):
    try:
        # Excel dosyasını oku (varsa) veya yeni bir dosya oluştur
        try:
            df = pd.read_excel(excel_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        # JSON verisini bir DataFrame'e çevir
        new_data = json.loads(json_data)
        new_df = pd.json_normalize(new_data)

        # DataFrame'i genişleterek birleştir
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

        # DataFrame'i Excel dosyasına yaz
        df.to_excel(excel_file, index=False)

        print("Veri başarıyla Excel dosyasına eklendi.")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")


class DatabaseHandler:
    def __int__(self):
        pass

    def add_data(self, data):
        json_to_excel(json_data=data, excel_file='data/veri.xlsx')
