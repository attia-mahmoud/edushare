//make a comment
function getDate (date) {
    first = date.substr(12, 4);
    second = date.substr(0, 10);
    date = first + " " + second;
    
    
    return date
}

function makeComment(data) {
    comment = document.createElement('p');
    date = getDate(data.fields.date);


    comment.innerHTML = `<div class="comment">
                            <img class="comment_pic" src="${data.fields.pic}">
                            <a href="../user_page/${data.fields.username}"><p class="comment_user">${data.fields.username}</p></a>
                            <p class="comment_date">${date}</p>
                            <p class="comment_content">${data.fields.content}</p>
                        </div>`
    document.getElementById('post_comments').append(comment);
}

//get all comments
function getComments(post_id) {
    console.log('sent');
    fetch(`http://127.0.0.1:8000/getcomments/${post_id}`)
            .then(response => response.json())
            .then(data => {
                

                document.getElementById('post_comments').innerHTML = '';
                for (var i = 0; i < data.length; i++) {
                    makeComment(data[i]);
                    
                    
                }
            })
}

//fetch user data
function fetchuser(type, post_id) {
    console.log("Going to fetch the user");
    console.log(type, post_id);
    type = "first";
    fetch(`../userdata/${type}/${post_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        photo = data[0].fields.profile_pic;
        document.getElementById("modal_pic").src = `../media/${photo}`;
    })
    type = "second";
    fetch(`../userdata/${type}/${post_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        name = data[0].fields.username;
        document.getElementById("modal_user").innerHTML = `Posted By: ${name}`;
    })
};

document.addEventListener("DOMContentLoaded", function() {
    

    //post modal
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className == 'post' || element.className == 'explore_posts'|| element.className == 'content_post') {
            
            post_id = element.dataset.id;
            
            try {
            name = element.getElementsByTagName('h6')[0].innerHTML;
            photo = element.getElementsByTagName('img')[0].src;
            }
            catch {
                name = ""
                photo = ""
            }
            //get the post content
            fetch(`/postmodal/${post_id}`)
            .then(response => response.json())
            .then(data => {
                
                post = data[0].fields;
                $("#postModal").modal()
                document.getElementById("modal_title").innerHTML = post.title;
                if (name && photo) {
                    document.getElementById("modal_user").innerHTML = `Posted By: ${name}`;
                    document.getElementById("modal_pic").src = photo;
                }
                date = getDate(post.date)
                document.getElementById('modal_date').innerHTML = date;
                document.getElementById('my_comment').innerHTML = '';
                if (post.subject != "Not Applicable") {
                    document.getElementById("modal_subject").style.display = "block";
                    document.getElementById("modal_subject").innerHTML = `${post.subject}`;
                    document.getElementById("subject_link").href = `../subject/${post.subject}`;
                }
                else{
                    document.getElementById("modal_subject").style.display = "none";
                };
                if (post.video) {
                    console.log("I have the video");
                    document.getElementById("modal_video").style.display = "block";
                    vid_id = "http://www.youtube.com/embed/" + post.video.split("?v=")[1];
                    document.getElementById("modal_video").src = vid_id;
                    console.log("I've placed the video");
                }
                else{
                    document.getElementById("modal_video").style.display = "none";
                };
                document.getElementById("modal_uni").innerHTML = `${post.university}`;
                document.getElementById("modal_desc").innerHTML = post.desc;
                if (post.doc != "null") {
                    document.getElementById("modal_url").style.display = "block";
                    document.getElementById("modal_url").href = `/media/${post.doc}`;
                }
                else {
                    document.getElementById("modal_url").style.display = "none";
                };
                document.getElementById("modal_title").innerHTML = post.title;
                document.getElementById("modal_type").innerHTML = post.post_type;
                document.getElementById("modal_div").setAttribute('data-id', data[0].pk)

            })
            
            type = "modal";
            fetchuser(type, post_id);
            
            //get the comments
            getComments(post_id);
            

        }
    });


    

    //like post
    document.addEventListener('click', event => {
        const element = event.target;
        classlists = element.classList
        if (element.classList.contains('numLikes')) {
            id = element.dataset.id;
            num_likes = element.innerHTML;
            console.log(num_likes);

            fetch(`/like/${id}`)
            .then(response => response.text())
            .then(data => {
                console.log(data);
                element.innerHTML = `${data[0]} &hearts;`;
                newvalue = element.innerHTML
                if (newvalue > num_likes){
                    element.classList.remove('not_liked');
                    element.classList.add('liked');
                }
                else{
                    element.classList.remove('liked');
                    element.classList.add('not_liked'); 
                }
            })
        }
    });

    //profile options
    function showPageProfile(id) {
        document.querySelectorAll('.profile_posts').forEach(div => {
            div.style.display = 'none';
            
        });
        document.querySelector(`#${id}`).style.display = 'block';
    };

    document.querySelectorAll('.profile_btn').forEach(button => {
       
        button.onclick = function() {
            document.querySelectorAll('.profile_btn').forEach(button => {
                button.classList.remove("chosen_button");
                
            })
            button.classList.add("chosen_button");
            showPageProfile(this.dataset.id);
        }
    });

    //user page options
    function showPageUser(id) {
        document.querySelectorAll('.user_divs').forEach(div => {
            div.style.display = 'none';
        });
        document.querySelector(`#${id}`).style.display = 'block';
    };

    document.querySelectorAll('.user_btn').forEach(button => {
       
        button.onclick = function() {
            document.querySelectorAll('.user_btn').forEach(button => {
                button.classList.remove("chosen_button");
            })
            button.classList.add("chosen_button");
            showPageUser(this.dataset.id);
        }
    });

    //make edit
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className == 'edit_button') {
            /*Assign Variables*/
            id = element.dataset.id;
            div = document.getElementById(id)
            title = div.getElementsByTagName('p')[0];
            description = div.getElementsByTagName('p')[1];
            /*Remove display*/
            description.style.display = "none";
            title.style.display = "none";
            /*Get innerHTML*/
            content = description.innerHTML;
            title_content = title.innerHTML;
            console.log(content, title_content);
            /*Create textareas */
            input1 = document.createElement('textarea');

            input1.setAttribute("id", `title${id}`);
            input1.classList.add('form-control');
            input1.innerHTML = title_content;
            div.appendChild(input1);

            input2 = document.createElement('textarea');
            input2.setAttribute("id", `input${id}`);
            input2.classList.add('form-control');
            input2.innerHTML = content;
            div.appendChild(input2);

            

            

            button = document.createElement('button');
            button.setAttribute("type", "submit");
            button.setAttribute("class", "save_button");
            button.setAttribute("data-saveid", id);
            button.innerHTML = "Save Edit";
            element.parentElement.appendChild(button);
            element.remove();

        }
    })

    //saveeditbutton
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className == 'save_button') {
            id = element.dataset.saveid;
            new_content = document.getElementById(`input${id}`).value;
            new_title = document.getElementById(`title${id}`).value;
            console.log(new_title, new_content);
            console.log("break")
            
            fetch(`/editpost/${new_content}/${new_title}/${id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                updated_title = document.getElementById(id).getElementsByTagName('p')[0];
                updated_content = document.getElementById(id).getElementsByTagName('p')[1];
                updated_title.innerHTML = data[0];
                updated_content.innerHTML = data[1];
                updated_title.style.display = "block";
                updated_content.style.display = "block";
                
                document.getElementById(`input${id}`).remove();
                document.getElementById(`title${id}`).remove();
                edit_button = document.createElement('button');
                edit_button.setAttribute("type", "button");
                edit_button.setAttribute("data-id", id);
                edit_button.classList.add("edit_button");
                edit_button.innerHTML = "Edit Post";
                element.parentElement.appendChild(edit_button);
                element.remove();
            })
        }
    })

    
    //Explore Sort By
    document.addEventListener('input', function (event) {

        if (event.target.id == 'sortBy'|| event.target.id == 'uniSort' || event.target.id == 'subjectSort') {
            sortBy = document.getElementById('sortBy').value; 
            uniSort = document.getElementById('uniSort').value; 
            subjectSort = document.getElementById('subjectSort').value; 
            console.log(sortBy, uniSort, subjectSort);
            fetch(`/sort/${sortBy}/${uniSort}/${subjectSort}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                document.querySelector('.allposts').innerHTML = "";
                if (data.length != 0) {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "Posts";
                    document.querySelector('.allposts').append(header);

                    for (var i = 0; i < data.length; i++) {
                        
                        
                        //new post
                        div = document.createElement('div');
                        
                        div.innerHTML = `<div data-id="${data[i].pk}" class="explore_posts">

                        
                        <!--<p class="explore_post__date">${data[i].fields.date}</p>-->
                        <p class="explore_type">${data[i].fields.post_type}</p>

                        
                        <p class="explore_post__title">${data[i].fields.title}</p>
                        
                        
                        <!--<a target="blank" href="media/${data[i].fields.doc}"><button class="btn btn-primary">Download File</button></a>-->
                        <p class="explore_stats">${data[i].fields.likes} &hearts;</p>
                        <p class="explore_stats">${data[i].fields.comments} <img class="explore_comments" src="static/app/comment.png"></p>
                        </div>`;
                    
                    //add post to DOM
                    document.querySelector('.allposts').append(div);

                    }
                }
                //if no posts match query, send error
                else {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "No posts match your filters.";
                    document.querySelector('.allposts').append(header);
                    img = document.createElement('img');
                    img.classList.add("vector");
                    img.src = "static/app/notfound.jpg";
                    document.querySelector('.allposts').append(img);
                }

            })
        }
    })



    //search funtion
    document.addEventListener('keyup', function (event) {
        if (event.target.id == 'search') {
            
            query = document.getElementById('search').value;
             if (query == "") {
                document.querySelector('.allposts').innerHTML = "";
                header = document.createElement('h2');
                header.classList.add("explore_header");
                header.innerHTML = "Use the dropdowns or search bar to find what you want.";
                document.querySelector('.allposts').append(header);
             }
            num = "first"
            fetch(`/search/${num}/${query}`)
            .then(response => response.json())
            .then(data => {
                
                document.querySelector('.allposts').innerHTML = "";
                if (data.length != 0) {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "Posts";
                    document.querySelector('.allposts').append(header);

                    for (var i = 0; i < data.length; i++) {
                        
                        
                        //new post
                        div = document.createElement('div');
                        
                        div.innerHTML = `<div data-id="${data[i].pk}" class="explore_posts">

                        
                        <!--<p class="explore_post__date">${data[i].fields.date}</p>-->
                        <p class="explore_type">${data[i].fields.post_type}</p>
                        <p class="explore_post__title">${data[i].fields.title}</p>
                        
                        
                        <!--<a target="blank" href="media/${data[i].fields.doc}"><button class="btn btn-primary">Download File</button></a>-->
                                <p class="explore_stats">${data[i].fields.likes} &hearts;</p>
                                <p class="explore_stats">${data[i].fields.comments} <img class="explore_comments" src="static/app/comment.png"></p> 
                        </div>`;
                    
                    //add post to DOM
                    document.querySelector('.allposts').append(div);

                    }
                }
                //if no posts match query, send error
                else {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "No posts match your filters.";
                    document.querySelector('.allposts').append(header);
                }
            })
            num = "second"
            fetch(`/search/${num}/${query}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.length != 0) {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "Users";
                    document.querySelector('.allposts').append(header);

                    for (var i = 0; i < data.length; i++) {
                        
                        
                        //new post
                        div = document.createElement('div');
                        
                        div.innerHTML = `<div class="explore_users">
                        <a href="user_page/${data[i].fields.username}"><h3>${data[i].fields.username}</h3></a>
                        
                        </div>`;
                    
                    //add post to DOM
                    document.querySelector('.allposts').append(div);

                    }
                } else {
                    header = document.createElement('h2');
                    header.classList.add("explore_header");
                    header.innerHTML = "No users match your query.";
                    document.querySelector('.allposts').append(header);
                }
            })
        }
    })


    //add comment
    if (document.getElementById('comment_btn')) {
    document.getElementById('comment_btn').onclick = function(event) {
        element = event.target;
        comment = document.getElementById("comment").value;
        document.getElementById("comment").value = '';
        post_id = element.parentElement.dataset.id;
        console.log(comment, post_id)
        fetch(`http://127.0.0.1:8000/add_comment/${post_id}/${comment}`)
        console.log('cleared');
        getComments(post_id);
        content = document.createElement('p');
        if (document.getElementById("numOfComments")) {
        document.getElementById("numOfComments").innerHTML = parseInt(document.getElementById("numOfComments").innerHTML) + 1;
        }
        if (comment == "") {
            document.getElementById('my_comment').innerHTML =  `<div class="comment">
                                                                <p class="comment_user" >Comment is invalid.</p>
                                                                
                                                            </div>`;
        }
        else {
            var utc = new Date().toJSON().slice(0,10).replace(/-/g,'-');
            var d = new Date().toLocaleTimeString('en-US', { hour12: true, 
                hour: "numeric", 
                minute: "numeric"});
            document.getElementById('my_comment').innerHTML = `<div class="comment">
                                                                <img id="comment_pic" class="comment_pic" src="">
                                                                <a id="comment_link" href=""><p id="comment_user" class="comment_user" ></p></a>
                                                                <p class="comment_date">${d} ${utc}</p>
                                                                <p class="comment_content">${comment}</p>
                                                            </div>`;
        }


        type = "third";
        fetch(`../userdata/${type}/${post_id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            photo = data[0].fields.profile_pic;
            document.getElementById("comment_pic").src = `../media/${photo}`;
        })

        type = "fourth";
        fetch(`../userdata/${type}/${post_id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            name = data[0].fields.username;
            document.getElementById("comment_user").innerHTML = name;
            document.getElementById("comment_link").href = `../user_page/${name}`
        })
        
    }
    }

    //delete comment

    

    document.querySelectorAll(".delete_icon").forEach(button => {
        button.onclick = function() {
            
            var id = button.dataset.id;
            var type = "comment";
            fetch(`../delete/${id}/${type}`)
            .then(response => response.text())
            .then(data=> {
                
            })
            button.parentElement.parentElement.style.display = 'none';
        };
    });

    //explore more

    
    
    //////////////////////////////////////////////////////////////////////////
    
    //dark mode
    /* Body */
const body = document.querySelector('body');

// Dark Mode Action
let darkMode = localStorage.getItem("darkMode");
const darkModeToggle = document.querySelector('.dark-mode-button');
const darkModeToggleFooter = document.querySelector('footer .dark-mode-button');
const nav = document.querySelector('nav');
// Enable Dark Mode
const enableDarkMode = () => {
    body.classList.add("dark-mode");
    localStorage.setItem("darkMode", "enabled")
    nav.classList.add("navbar-dark")
    nav.classList.add("bg-dark")
    
}

// Disable Dark Mode
const disableDarkMode = () => {
    body.classList.remove("dark-mode");
    localStorage.setItem("darkMode", null)
    nav.classList.remove("navbar-dark")
    nav.classList.remove("bg-dark")
}

if (darkMode == "enabled") {
    enableDarkMode();
}

// Desktop Button
darkModeToggle.addEventListener('click', () => {
    darkMode = localStorage.getItem("darkMode");
    if (darkMode !== "enabled") {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
})

// Footer button, optional. This is for if you have a second dark mode toggle button
//in the footer, just make sure the button is inside the footer tag, and it will be
//linked to this function.

    darkModeToggleFooter.addEventListener('click', () => {
        darkMode = localStorage.getItem("darkMode");
        if (darkMode !== "enabled") {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    })

    

})

