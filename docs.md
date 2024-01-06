## APIs:

```
GET /images/className
```
Gets all the images in the database

```
DELETE /images/className 
```
Deletes all words in the database with archiving solution. 


```
DELETE /image/{imageName}
```
Deletes a particular image in the database
E.g `DELETE /image/cat` will image 'cat'

If the image is not found in the database, return a 404 error.

```
POST /images/className
{
  images:[]
}
```
Adds the images in the DB
