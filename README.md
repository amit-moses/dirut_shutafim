Dirot-shutafim
Models:
1.	User

2.	Apartment
•	id
•	Publisher (fk)
•	city 
•	street
•	rent_price
•	floor
•	partners
•	gender
•	entry_date
•	details
•	title 
•	kosher
•	agree_mail
•	type

-	get_url – return the url of singlepage view of apartment.
-	short_title / short_ details – return short data for preview page.
-	get_date_format – return the entrey date as 'dd/mm/yyyy' format.
-	toJSON – return json object of this apartment.
-	delete_1_image – delete the image which entered.
-	updateImages_1 – delete every image which deleted by the user.
-	make_random_name – select random key for file name in firebase
-	uploadImages – upload every image in the images list to imagedata model and upload to firebase
-	updateImages (updateImages_1 + uploadImages)
-	deleteAllImages – deletes all the images of this apartment from imagedata model and from firebase
  
3.	ImageData
•	Id
•	apartment (fk)
•	myurl

-	index – get the index of this image according to the order of uploading. 