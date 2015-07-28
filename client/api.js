var base = "http://localhost:4000/"

function httpGet(url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function getUserInfo(user)
{
    var url = base + "api?action=userinfo&id=" + user
    
    var result = JSON.parse(httpGet(url))

    if (!result.success)
    {
        return null;
    }
    
    return result
}

/*
 * firstName, lastName and id must be URL-safe.
 * */
function createNewUser(firstName, lastName, id)
{
    var url = base +
              "api?action=newuser&firstname=" +
              firstName +
              "&lastname=" +
              lastName +
              "&id=" +
              id

    var result = JSON.parse(httpGet(url))
    
    return result.success
}

function deleteUser(id)
{
    var url = base + "api?action=deleteuser&id=" + id
    
    var result = JSON.parse(httpGet(url))
    
    return result.sucess
}

/*
 * radius is in miles.
 * longitude and latitude are in degrees.
 * */
function searchPlaces(longitude, latitude, radius)
{
    var url = base +
              "api?action=findplaces&longitude=" +
              longitude.toString() +
              "&latitude=" +
              latitude.toString()) +
              "&radius=" +
              radius.toString()

    var result = JSON.parse(httpGet(url))

    if (!result.success)
    {
        return null;
    }
    
    return result.places
}

function getScoreboard(num)
{
    var url = base + "api?action=scoreboard&num=" + num.toString()

    var result = JSON.parse(httpGet(url))

    if (!result.success)
    {
        return null
    }
    
    return result.users
}

function updateUser(user, place)
{
    var url = base + "api?action=updateuser&user=" + user + "&place=" + place
    
    var result = JSON.parse(httpGet(url))

    return result.success
}
