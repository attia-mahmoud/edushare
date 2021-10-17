# Edushare

## Abstract

This project is called EduShare and its main aim is to provide a platform, mainly targeted towards college and university level students, where users can gain help and knowledge as well as provide other students with the same through asking questions, sharing content, or simply expressing their opinions.

There are many websites out there that provide educational content or act as a question/answer forum but rarely do we find ones that do both. This website tries to do just that.

**The biggest focus was on creating a smooth and likable user experience and design as well as provide features users would deem convenient on a social network.** The UI is simple and intuitive and doesn't overwhelm users with too many features thrown at them. Additionally, the UX allows for comfortable surfing with easy access to whatever the user is looking for.

This website does not aim to be a social network, however it adopts some useful and critical features from one.

### Why I believe this project satisfies the distinctiveness and complexity requirements
One challenge I faced during the production of this website was allowing the vast majority of features to run in real-time, without the need to reload the page. One way this problem was overcome was by continually retrieving data from the back-end every time the user would perform a new action, such as typing a query in the search bar on the explore page or adding an answer under a question. Afterward, I would display the data onto the DOM all without reloading the page.

The website aimed to provide a minimalistic and eye-pleasing visual aesthetic which may compensate any lack of sophistication in the back-end.


## Layout
### Pages
- Home page
- Explore page
- Subject page
- User feed 
- User account pages
- Profile page
### Navigation bar 
A side navigation bar is presented in desktop view and a top navigation bar in mobile view. 
The side navigation bar is partially hidden until the user hovers over it to avoid it hindering the user's view.

### Sidebars
The left sidebar displays a vertical navigation bar, only visible in desktop mode.  
The right sidebar displays other EduShare users to potentially follow and a selection of the latest posts for quick discovery and access.

Sidebars are fixed in position to allow for convenient and efficient surfing of the site as it allows visitors to smoothly flow from one section of the site to another with little to no scrolling or searching.
### Footer
Displays copyright info  
Contains links to the website's pages for user convenience

### Back to top button
Allows the user to quickly return to the top of the page without making too much effort. This can be very useful when the page has a lot of content.

## Features

### Security
Users who are not logged in may not download files, create posts, follow users, or like or comment on any posts.   
Users may not change or alter anything on other users' accounts.
### Dark Mode
Removes contrast issues and accommodates those who wish to view everything with less brightness and harsh white light. 
Affects the whole website.

### Mobile-responsive
Accommodates users who wish to view the website on smaller screens (specifically <768px) such as their mobiles or tablets.

### Pagination
Maximum 10 posts per page (for pages that contain posts), then users must jump to the next set of posts.  
Improves navigation experience and allows for greater organization of the webpage.

### Adding Content
Posts could be made to ask questions, share content such as videos or files, or simply to start a rant (because we all know how much college students love ranting)

#### Posts must include: 
- Post type
- Title
- Description
- Subject
- University
- University Level
#### Posts may include:
- An attached pdf file
- Embedded youtube video

## Post/Content Features
### Modal
Clicking on a post that contains shared content opens a modal where the user may view the post more comfortably.
### Tags
Displayed at the top of the modal indicating the **post type** in addition to the **university** and **subject** of the post so that the user knows precisely what he's looking at.
Additionally, the subject tag may be clicked on which will lead the user to the respective subject page where users can view additional content under that subject.
### Users have the ability to:
- like posts
    - number of likes and color change in real-time
- comment or provide an answer under each post
  - counter updates and comments appear in real-time
  - an empty comment presents an error to the user
- click on the username of those who commented to visit their user page
- click on the poster's username to visit his/her user page
- download files the poster has linked
- watch an embedded youtube video the poster has linked


## Subject Page
After choosing a subject the user is redirected to the respective subject page where he/she can view all questions, videos, and files shared under that subject.

## Explore Page
Users can choose to use the **dropdown menus** to filter and find new posts based on the posts':
- popularity
- date posted
- university
- subject
  
Additionally, users can use the **search bar** to search specific keywords and/or look for other users based on their username.

An error is presented if no posts match the specified filters or keywords.

## User's Feed
Here users can view the posts of other users which they are interested in and have followed.

## User Page
#### For each user, this page displays:
- user's profile picture and username
- number of followers user has
- number of users the user follows
- number of posts the user has
- follow/unfollow button
- user's bio
#### Options are displayed where you can choose to view:
- all posts the user has posted
- all files the user has uploaded
- all videos the user has linked
## Profile Page
#### This page displays only for the logged in user:
- user's profile picture and username
- number of followers user has
- number of users the user follows
- number of posts the user has
- user's bio

#### Options are displayed where user can choose to view:
- account details
- all posts the user has posted
- all posts the user has liked
- all comments the user has commented

#### User has the ability to change to his/her liking the:
- username
- email
- profile picture
- bio

User can edit the title and description of each post

User has the ability to view and delete any of his/her previous comments

## Project Files

### Python Files          
**urls.py**       
where all web routes were stored   

**views.py**         
where calls to the URLs were handled  
        
**models.py**           
where models were stored         

Models used in this project:
- User; derived from AbstractUser
- Profile
- Posts
- Likes
- Follow
- Comments

**forms.py**     
where forms were created 

Forms used in this project:
- UserForm
- ProfileForm
- PostForm
- UserUpdateForm
- ProfileUpdateForm

### Webpages
**layout.html**  
defines the base layout of the website          
 
**login.html**  
the login page           

**register.html**  
the registration page 
       
**index.html**  
home page  

**subject.html**  
main page for each subject; contains questions, videos, and files for the respective subject

**post.html**  
where a user can view a specific question and provide an answer for it
  
**explore.html**  
where users can search for and discover new posts and users         
  
**following.html**  
user's feed       
 
**profile.html**  
profile page of the active user           
  
**user.html**  
user page for each user on the website  

### Stylesheets

**styles.css**  
base CSS file        

**dark.css**  
used to configure dark mode

### Javascript Files
**javascript.js**  
used to add user interactivity as well as perform calls to the back-end


