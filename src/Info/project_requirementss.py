
#########################################################################################
#########################################################################################
#############                        Star Wars Blog                         #############
#############                           REST API                            #############
#############                   Endpoints - REQUIREMENTS                    #############
#########################################################################################
#########################################################################################

"""
    |-----------------------------------------------------------------------------------
    |-----------------  4GEEKS PROJECT INSTRUCTIIONS AND REQUIREMENTS  -----------------
    |-----------------------------------------------------------------------------------
    |
    |
    |       -- [GET] info from PEOPLE and PLANETS --
    |
    |-----------
    |    People's information:
    |        [] Get list of ALL PEOPLE ----------------> [GET] /people
    |        [] Get ONE PERSON ------------------------> [GET] /people/<int:people_id>
    |-----------
    |    Planets' information:
    |        [] Get list of ALL PLANETS ---------------> [GET] /planets
    |        [] Get ONE PLANET ------------------------> [GET] /planets/<int:planet_id>
    |
    |
    |-----------------------------------------------------------------------
    |
    |
    |       -- CRUD operations: Users and Favorites --
    |
    |-----------
    |    [GET] User's information:
    |        [] Get list of ALL USERS -----------------> [GET] /users
    |        ¿¿?? MISSING INFO OF JUST ONE USER -------> ¿¿¿¿¿????? ---> [GET] /users/<int:user_id>
    |
    |-----------
    |    Favorites from CURRENT USER:
    |        [] ALL Favorites, current user -----------> [GET] /users/favorites
    |
    |-----------
    |    Adding new favorites:
    |        [] Add One PLANET ------------------------> [POST] /favorite/planet/<int:planet_id>
    |        [] Add One PEOPLE ------------------------> [POST] /favorite/people/<int:people_id>
    |
    |-----------
    |    Deleting favorites:
    |        [] Delete One PLANET ---------------------> [DELETE] /favorite/planet/<int:planet_id>
    |        [] Delete One PEOPLE ---------------------> [DELETE] /favorite/people/<int:people_id>
    |
    |
    |-----------------------------------------------------------------------
    |
    |
    |       -- EXTRA POINTS: [POST], [PUT] and [DELETE]  Planets and People --
    |
    |      "+4 Create also endpoints to add (POST), update (PUT), and delete (DELETE) planets and people.
    |       That way all the database information can be managed using the API instead of having to rely on
    |       the Flask admin to create the planets and people."
    |
    |-----------
    |    [POST], [PUT] and [DELETE]  Planets:
    |        [] Add one PLANET ------------------------> [POST]   /planets
    |        [] Update one PLANET ---------------------> [PUT]    /planets/<int:planet_id>
    |        [] Delete one PLANET ---------------------> [DELETE] /planets/<int:planet_id>
    |
    |-----------
    |    [POST], [PUT] and [DELETE]  People:
    |        [] Add one PEOPLE ------------------------> [POST]   /people/
    |        [] Update one PEOPLE ---------------------> [PUT]    /people/<int:people_id>
    |        [] Delete one PEOPLE ---------------------> [DELETE] /people/<int:people_id>
    |
    |---------------------------------------------------------------------------------------------------
"""