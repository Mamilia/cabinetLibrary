# cabinetLibrary

This is a dynamic and responsive Django web application that works as a digital plataform for users to share videos, images, documents, and comments. It's originally designed for academic purposes within a class of students. It's structured in 4 main categories named: 'Reading Material', 'Film and Videos', 'Images gallery' and 'Chat room' For register as a user the student most have a predetermined key that is defined by the admin in the Key module

In views.py:

-The subcategoy function is where the display of each category is defined as well as taking care of the POST methods of each form in them.
-The search and search_subcategoy functions are, respectively, a global and local search engine for the Reading Material's category.
-The pagination of each subcategory is imported from the config.py module, located in the .examples directory. The html for this is written in the layout.html module.
-The bananaLike, delete_reading, edit and editReview functions are handling the internal API calls of the readings likes, the delete of the readings, the edit of the posts and the edit of the readings reviews, respectively. These calls come from the fetch API promises written in the javascript's modules.

Users are also able to create their own subcategories in each of the 4 main categories. To start this website the admin must create the 4 main categories with their respective names as well as at least one subcategory per category.

This project completly fullfil the funcionality necessary for group of users to share videos, images and documents among themselves, that helps them exchange, organize and store information and comments. It has an administrator interface that facilitates the management of the users, the information published and the main Key required for register as a user.
