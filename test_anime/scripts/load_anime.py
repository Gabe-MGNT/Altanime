from search_anime.models import Anime
import csv
import os
csv.field_size_limit(256<<10)
def run():
    with open('anime.csv', encoding='utf8') as file:
        reader = csv.reader(file)
        next(reader)

        Anime.objects.all().delete()

        for row in reader:
            #print(row)

            if row[22]=='id':
                continue


            anime = Anime(
                title = row[-1],
                summary=row[-2],
                aired_date=row[0],
                episodes = row[7],
                favorites = row[8],
                status = row[18],
                studios = row[19],
                themes = row[20],
                type = row[21],
                id = row[22],
                popularity = row[24],
                ranking = row[25],

            )


            image_path = os.path.join("img", str(row[22]), "large_image_url-1.jpg")

            print("imgae_path : ", image_path)

            if os.path.isfile(image_path):
                with open(image_path, 'rb') as file:
                    anime.image.save(f'{anime.id}.png', file, save=True)


            anime.save()