document.addEventListener('DOMContentLoaded', ()=>{

	if(document.querySelector('#username')){
		username = document.querySelector('#username').innerHTML;
		//this function tells what posts are already liked by the user
		post_liked(username);

		document.querySelectorAll('#like').forEach(i =>{
			i.onclick = ()=>{
				postid = i.dataset.postid;
				no_likes = document.querySelector(`#p${postid}`).innerHTML;
				postadmin = i.dataset.username
				if(i.className === "fa fa-heart unactive"){
					i.className = "fa fa-heart active";
					flag = 0;
					fetch(`/likes/${postid}/${postadmin}/${flag}`)
					.then(response => response.text())
			        .then(text => {
			            console.log(text);
			        });
					no_likes = parseInt(no_likes) +1
					document.querySelector(`#p${postid}`).innerHTML = no_likes;
				}
				else{
					i.className = "fa fa-heart unactive";
					flag = 1;
					fetch(`/likes/${postid}/${postadmin}/${flag}`)
					.then(response => response.text())
			        .then(text => {
			            console.log(text);
			        });
					no_likes = parseInt(no_likes) - 1
					document.querySelector(`#p${postid}`).innerHTML = no_likes;
				}
			};
		});

		if (document.querySelector("#follow")) {
			//this functions tell is the user already follows the other user
			followings(document.querySelector("#follow").dataset.name, document.querySelector("#follow"));
			document.querySelector("#follow").onclick = function(){
				if (this.className === "btn btn-outline-primary") {
					flag = 0;
					this.className = "btn btn-outline-success";
					this.innerHTML = "Following";
					document.querySelector('#followers').innerHTML = parseInt(document.querySelector('#followers').innerHTML) + 1;
					const request = new XMLHttpRequest();
					request.open('GET', `/follow/${this.dataset.name}/${flag}`);
					request.onload = ()=>{
						console.log("loading");
						res = (request.response).toString();
					}
					request.send();
				}
				else{
					flag = 1;
					this.className = "btn btn-outline-primary";
					this.innerHTML = "Follow";
					document.querySelector('#followers').innerHTML = parseInt(document.querySelector('#followers').innerHTML) - 1;
					const request = new XMLHttpRequest();
					request.open('GET', `/follow/${this.dataset.name}/${flag}`);
					request.onload = ()=>{
						console.log("loading");
						res = (request.response).toString();
					};
					request.send();
				}
			};
		}
		if(document.querySelector('#formEle')){
			document.querySelector('#formEle').onsubmit = function(e){
				e.preventDefault();
				return false;
			}
		}
		if(document.querySelector('#editpost')){
			//on clicking edit post button
			document.querySelector('#editpost').onclick = function(){
				console.log("im clickeds")
				postid = this.dataset.postid;
				admin = this.dataset.username;
				//hide the original post div
				document.querySelector(`#postdiv${postid}`).style.display = "none";
				//display edit post div
				document.querySelector(`#editpostdiv${postid}`).style.display = "block";
				
				//on clicking the save button send request to the server without reloading page
				document.querySelector(`#savebtn${postid}`).onclick = function(){
					newpost = document.querySelector(`#textarea${postid}`).value;
					form = new FormData(formEle);
					form.append("id", postid);
					form.append("post", newpost);
					form.append("admin", admin);
					//display the edited post
					document.querySelector(`#postdiv${postid}`).style.display = "block";
					document.querySelector(`#posttext${postid}`).innerHTML = newpost;
					document.querySelector(`#editpostdiv${postid}`).style.display = "none";
					const csrftoken = getCookie('csrftoken');
					const request = new Request(
					    "/editpost",
					    {headers: {'X-CSRFToken': csrftoken}}
					);
				  	fetch(request, {
				  		method: "POST",
				  		mode: 'same-origin',
					    body: form,
					}).then(response => response.text())
			        .then(text => {
			            console.log(text);
			        });
					}
			};
		}
	}
});

function followings(name, element){
	const request = new XMLHttpRequest();
	request.open('GET', `/followings/${name}`);
	request.onload = ()=>{
		console.log("loading");
		res = (request.response).toString();
		if (res === "Yes") {
			element.className = "btn btn-outline-success";
			element.innerHTML = "Following";
		}
	}
	request.send();
}

function post_liked(username){
	const request = new XMLHttpRequest();
	request.open('GET', `/postliked/${username}`);
	request.onload = ()=>{
		console.log("loding")
		res = JSON.parse(request.response);
		document.querySelectorAll('#like').forEach(i =>{
			postid = i.dataset.postid;
			for (var j = 0; j <res.length; j++) {
				if(parseInt(res[j]) === parseInt(postid)){
					i.className = "fa fa-heart active"
				}
			}
			
		});
	}
	request.send();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}