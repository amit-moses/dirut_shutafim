Dirot-shutafim
Models:
1.	User (default Django)

2.  Apartment
•   id
•   Publisher (fk)
•   city 
•   street
•   rent_price
•   floor
•   partners
•   gender	
•   entry_date
•   details
•   title 
•   kosher
•   agree_mail
•   type
•   update

-   get_url – return the url of singlepage view of apartment.
-   short_title / short_ details – return short data for preview page.
-   get_date_format – return the entrey date as 'dd/mm/yyyy' format.
-   toJSON – return json object of this apartment.
-   delete_1_image – delete the image which entered.
-   updateImages_1 – delete every image which deleted by the user.
-   make_random_name – select random key for file name in firebase
-   uploadImages – upload every image in the images list to imagedata model and firebase
-   updateImages (updateImages_1 + uploadImages)
-   deleteAllImages – deletes all images of this apartment from imagedata model and firebase
-   set_update – define the current time as update time
-   is_update – return if past more than 24 hours since the ad has updated
  
3.  ImageData
•   Id
•   apartment (fk)
•   myurl

-   index – get the index of this image according to the order of uploading. 


4.  Messages

•   Id
•   user_to (fk)
•   apartment (fk)
•   pub_date
•   mes_content
•   mes_from
•   mes_contact
•   mes_read

-   read_set - SET message as read and return the value before the action.
-   get_date_format - return format of sending date message as 'dd/mm/yy H:M'
-   get_new_mes - get the number of unread messages of this user who got this message
-   get_all_mes - get all messages of this user which orded from the newest.
