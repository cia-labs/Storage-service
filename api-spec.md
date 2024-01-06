## APIs:

```
GET /images/className
```
1. Gets all the images in the database

```
DELETE /images/className 
```
2. Deletes all words in the database with archiving solution. 


```
DELETE /image/{imageName}
```
3. Deletes a particular image in the database
E.g `DELETE /image/cat` will image 'cat'

If the image is not found in the database, return a 404 error.

```
POST /images/className
{
  images:[]
}
```
4. Adds the images in the DB
