import tmdbsimple as tmdb
tmdb.API_KEY = '4917b326d31e3b3a5b77c40fa3256ecf'

def getMovies():
    movies_response = tmdb.Movies()
    popular = movies_response.popular()
    movies = popular['results']

    genre_response = tmdb.Genres()
    genres = genre_response.movie_list()['genres']

    images = tmdb.Movies(movies[0]['id']).images(include_image_language='en,null')
    info = tmdb.Movies(movies[0]['id']).info()
    movies[0].update({'images': images, 'info': info})

    for movie in movies:
            providers_response = tmdb.Movies(movie['id']).watch_providers()
            
            if 'results' in providers_response and 'US' in providers_response['results'] and 'buy' in providers_response['results']['US']:
                providers = providers_response['results']['US']['buy']
            else:
                providers = 'No provider yet'

            genre_names = []
            for genre in genres:
                if genre['id'] in movie['genre_ids']:
                    genre_names.append(genre['name'])

            movie.update({'genre_names': genre_names, 'providers': providers})

    return movies

