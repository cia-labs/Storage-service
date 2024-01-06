## APIs:
1. Gets all the images in the database
```
GET /images/className
```

2. Deletes all words in the database with archiving solution. 
```
DELETE /images/className 
```

3. Deletes a particular image in the database
E.g `DELETE /image/cat` will image 'cat'
```
DELETE /image/{imageName}
```
If the image is not found in the database, return a 404 error.

4. Adds the images in the DB
```
POST /images/className
{
  images:[]
}
```

