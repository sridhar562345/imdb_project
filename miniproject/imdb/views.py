from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def index(request):
    movie_list = Movie.objects.all()
    context = {'movie_list':movie_list}
    return render(request,'imdb_home.html',context)

def movie(request,movie_id):
    movie_obj = Movie.objects.get(id = movie_id)
    cast_list = Cast.objects.filter(movie = movie_obj)
    context = {'movie':movie_obj,'cast_objs':cast_list}
    return render(request,'imdb_movie.html',context)

def director(request,director_id):
    movie_director = Director.objects.get(id = director_id)
    movies = movie_director.movie_set.all()
    context = {'director':movie_director,'movies':movies}
    return render(request,'imdb_director.html',context)

def actor(request,actor_id):
    actor_obj = Actor.objects.get(id = actor_id)
    movies_list = actor_obj.movie_set.all()
    context = {'actor':actor_obj,'movies':movies_list}
    return render(request,'imdb_actor.html',context)

def analytics(request):
    import json
    bar_data = get_one_bar_plot_data()
    pie_data = get_pie_chart_data()
    two_bar_data = get_two_bar_plot_data()
    polar_chart = get_polar_chart_data()
    multi_line_plot = get_multi_line_plot_data()
    sri = sri_get_one_bar_plot_data()
    data = {}
    data.update(bar_data)
    data.update(pie_data)
    data.update(two_bar_data)
    data.update(polar_chart)
    data.update(multi_line_plot)
    data.update(sri)
    return render(request,'analytics.html',context=data)



def get_one_bar_plot_data():
    import json
    from .models import Movie
    query1 = """select Avg(box_office_collection_in_crores) from imdb_movie group by movie_year having movie_year between 2010 and 2015 order by movie_year asc;"""
    query2 = """select distinct movie_year from imdb_movie where movie_year between 2010 and 2015 order by movie_year asc;"""
    averages = execute_sql_query(query1)
    years = execute_sql_query(query2)
    single_bar_chart_data = {
        "labels": list(years),
        "datasets":[
            {
                "data": list(averages),
                "name": "Single Bar Chart",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "border_width": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)"
            }
        ]
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'Average B.O collections per year'
    }

def sri_get_one_bar_plot_data():
    import json
    from .models import Movie
    query1 = """select Avg(box_office_collection_in_crores) from imdb_movie group by movie_year having movie_year between 2010 and 2015 order by movie_year asc;"""
    query2 = """select distinct movie_year from imdb_movie where movie_year between 2010 and 2015 order by movie_year asc;"""
    averages = execute_sql_query(query1)
    years = execute_sql_query(query2)
    single_bar_chart_data = {
        "labels": list(years),
        "datasets":[
            {
                "data": list(averages),
                "name": "Single Bar Chart",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "border_width": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)"
            }
        ]
    }
    return {
        'sri_single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'sri_single_bar_chart_data_one_title': 'Average B.O collections per year'
    }


def get_pie_chart_data():
    import json
    from .models import Movie
    query_1 = """
                select AVG(box_office_collection_in_crores) from imdb_movie group by genre order by genre asc;
                """

    query_2 = """select distinct genre from imdb_movie order by genre asc;"""

    counts = execute_sql_query(query_1)
    genres = execute_sql_query(query_2)

    pie_chart_data = {
        "datasets": [{
            "data": list(counts),
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": list(genres)
    }

    return {
        'pie_chart_data_one': json.dumps(
            pie_chart_data),
        'pie_chart_data_one_title': 'Movies and B.O collections'
    }


def get_polar_chart_data():
    import json
    query1 = """select AVG(`movie`.box_office_collection_in_crores) as average,`director`.name from imdb_movie as movie,
        imdb_director as director where `movie`.director_id = `director`.id
        group by `director`.id
        order by average desc limit 5;"""
    data = execute_sql_query(query1)
    directors = []
    average_collections = []
    for i in data:
        directors.append(i[1])
        average_collections.append(i[0])
    
    polar_chart_data = {
        "datasets": [{
            "data": average_collections,
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.8)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0,0,0,0.2)",
                "rgba(0, 123, 255,0.5)"
            ]

        }],
        "labels": directors
    }
    return {
        'polar_chart_data_one': json.dumps(
            polar_chart_data),
        'polar_chart_data_one_title': 'Director and his average collections'
    }

def get_two_bar_plot_data():
    import json
    query_1 = """select count(Distinct actor.id) from imdb_cast as cast,imdb_actor as actor,imdb_movie as movie
                where `actor`.id=`cast`.actor_id and `movie`.id=`cast`.movie_id and `actor`.gender='male'
                group by `movie`.movie_year having `movie`.movie_year between 2013 and 2018 order by movie.movie_year asc;"""

    query2 = """
                select count(Distinct actor.id) from imdb_cast as cast,imdb_actor as actor,imdb_movie as movie
                where `actor`.id=`cast`.actor_id and `movie`.id=`cast`.movie_id and `actor`.gender='female'
                group by `movie`.movie_year having `movie`.movie_year between 2013 and 2028 order by movie.movie_year asc;
                """

    query_3 = """
                select distinct movie_year from imdb_movie  WHERE movie_year between 2013 and 2018 order by movie_year asc;
                """
    males = execute_sql_query(query_1)
    females = execute_sql_query(query2)
    years = execute_sql_query(query_3)
    multi_bar_plot_data = {
        "labels": list(years),
        "datasets": [
            {
                "label": "Male",
                "data": list(males),
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)",
                "fontFamily": "Poppins"
            },
            {
                "label": "Female",
                "data": list(females),
                "borderColor": "rgba(0,0,0,0.09)",
                "borderWidth": "0",
                "backgroundColor": "rgba(0,0,0,0.07)",
                "fontFamily": "Poppins"
            }
        ]
    }

    return {
        'multi_bar_plot_data_one': json.dumps(multi_bar_plot_data),
        'multi_bar_plot_data_one_title': 'Male and Female actors'
    }



def get_multi_line_plot_data():
    import json
    query_1 = '''select box_office_collection_in_crores,budget_in_crores,name from imdb_movie group by name
                order by average_rating desc limit 5;'''
    data = execute_sql_query(query_1)
    collections = []
    budget = []
    movie_name = []
    for i in data:
        collections.append(i[0])
        budget.append((i[1]/10000000))
        movie_name.append(i[2])
    multi_line_plot_data = {
        "labels": movie_name,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "label": "B.O collections",
            "data": collections,
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(220,53,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(220,53,69,0.75)',
        }, {
            "label": "Budget",
            "data": budget,
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(40,167,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(40,167,69,0.75)',
        }]
    }
    return {
        'multi_line_plot_data_one': json.dumps(multi_line_plot_data),
        'multi_line_plot_data_one_title': 'Top Movies and details'
    }    


def execute_sql_query(sql_query):
    """
    Executes sql query and return data in the form of lists (
        This function is similar to what you have learnt earlier. Here we are
        using `cursor` from django instead of sqlite3 library
    )
    :param sql_query: a sql as string
    :return:
    """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    return rows



def populate_database():
    actors_list=[
        {
            "actor_id": "6",
            "name": "Emma_Watson",
            "dob" : "2010-07-16",
            
            "gender":'F'
        },
        {
            "actor_id": "5",
            "dob" : "2010-07-16",
            "name": "Robert Pattinson",
            
            "gender":'M'
        },
        {
            "actor_id": "4",
            "dob" : "2010-07-16",
            "name": "Daniel Radcliffe",
            
            "gender":'M',
        },
        {
            "actor_id": "3",
            "dob" : "2010-07-16",
            "name": "Paul Walker",
            
            "gender":'M'
        },
        {
            "actor_id": "2",
            "dob" : "2010-07-16",
            "name": "Leonardo DiCaprio",
            
            "gender":'M'
        },
        {
            "actor_id": "1",
            "dob" : "2010-07-16",
            "name": "Robert Downey, Jr",
            
            "gender":'M'
        },
        {
            "actor_id": "7",
            "dob" : "2010-07-16",
            "name": "Prabhas Raj",
            
            "gender":'M'
        }
    ]
    movies_list= [
        {
            "movie_id": "5",
            "name": "inception",
            "actors": [
                {
                    "actor_id": "2",
                    "role": "Hero",
                    "is_debut_movie": False,
                    "remuneration_in_crores":30
                }
            ],
            "box_office_collection_in_crores": 150,
            "release_date": "2010-07-16",
            "director_name": "Christopher Nolen",
            "budget_in_crores" : 100,
            "rank":8,
            "genre":"scifi",
            "runtime_minutes":145,
            "votes" : 100020,
            "movie_year":2010

        },
        {
            "movie_id": "4",
            "name": "Twilite saga",
            "actors": [
                {
                    "actor_id": "5",
                    "role": "Hero",
                    "is_debut_movie": False,
                    "remuneration_in_crores":25
                }
            ],
            "box_office_collection_in_crores":75 ,
            "release_date": "2013-03-02",
            "director_name": "Catherine Hardwicke",
            "budget_in_crores" : 90,
            "rank":7,
            "genre":"Thriller",
            "runtime_minutes":150,
            "votes" : 100020,
            "movie_year":2013
        },
        {
            "movie_id": "3",
            "name": "Fast&furious",
            "actors": [
                {
                    "actor_id": "3",
                    "role": "Hero",
                    "is_debut_movie": False,
                    "remuneration_in_crores":30
                }
            ],
            "box_office_collection_in_crores":100 ,
            "release_date": "2001-06-22",
            "director_name": "James Wan",
            "budget_in_crores" : 100,
            "rank":8,
            "genre":"Horror",
            "runtime_minutes":155,
            "votes" : 100000,
            "movie_year":2001
        },
        {
            "movie_id": "2",
            "name": "Harry Potter",
            "actors": [
                {
                    "actor_id": "4",
                    "role": "Hero",
                    "is_debut_movie": False,
                    "remuneration_in_crores":30
                },
                {
                    "actor_id": "6",
                    "role": "Heroine",
                    "is_debut_movie": False,
                    "remuneration_in_crores":20
                }
            ],
            "box_office_collection_in_crores":500 ,
            "release_date": "2002-04-12",
            "director_name": "David Yates",
            "budget_in_crores" : 170,
            "rank":9,
            "genre":"scifi",
            "runtime_minutes":150,
            "votes" : 100020,
            "movie_year":2002
        },
        {
            "movie_id": "1",
            "name": "IronMan",
            "actors": [
                {
                    "actor_id": "1",
                    "role": "Hero",
                    "is_debut_movie": False,
                    "remuneration_in_crores":40
                }
            ],
            "box_office_collection_in_crores":700 ,
            "release_date": "2010-05-01",
            "director_name": "Jon Favreau",
            "budget_in_crores" : 250,
            "rank":10,
            "genre":"scifi",
            "runtime_minutes":165,
            "votes" : 1000020,
            "movie_year":2010
        },
        # {
        #     "movie_id": "",
        #     "name": "",
        #     "actors": [
        #         {
        #             "actor_id": "",
        #             "role": "",
        #             "is_debut_movie": False
        #         }
        #     ],
        #     "box_office_collection_in_crores": ,
        #     "release_date": "",
        #     "director_name": ""
        # }
    ]
    directors_list= [
        "Christopher Nolen",
        "Catherine Hardwicke",
        "James Wan",
        "David Yates",
        "Jon Favreau"
    ]
    movie_rating_list= [
        {
            "movie_id": "1",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        },
        {
            "movie_id": "2",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        },
        {
            "movie_id": "3",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        },
        {
            "movie_id": "4",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        },
        {
            "movie_id": "5",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        }
    ]
    for actor in actors_list:
        Actor.objects.create(actor_id = actor["actor_id"],name=actor["name"],dob=actor["dob"],gender = actor["gender"])
        
        
    for director in directors_list:
        Director.objects.create(name=director)
    
    
    for movie in movies_list:
        movie_object = Movie.objects.create(name=movie["name"],
        movie_id = movie["movie_id"],
        release_date = movie["release_date"],
        box_office_collection_in_crores = movie["box_office_collection_in_crores"],
        director= Director.objects.get(name=movie["director_name"]),
        budget_in_crores=movie["budget_in_crores"],
        runtime_Minutes=movie["runtime_minutes"],
        rank=movie["rank"],
        genre=movie["genre"],
        votes=movie["votes"],
        movie_year = movie["movie_year"])
        
        cast_list = movie["actors"]
        for cast in cast_list:
            Cast.objects.create(actor = Actor.objects.get(actor_id=cast["actor_id"]),
            movie=movie_object,
            role = cast["role"],
            is_debut_movie = cast["is_debut_movie"],remuneration_in_crores=cast["remuneration_in_crores"])
    
    
    for rating in movie_rating_list:
        Rating.objects.create(movie=Movie.objects.get(movie_id=rating["movie_id"]),
        rating_one_count = rating["rating_one_count"],
        rating_two_count = rating["rating_two_count"],
        rating_three_count = rating["rating_three_count"],
        rating_four_count = rating["rating_four_count"],
        rating_five_count = rating["rating_five_count"])



