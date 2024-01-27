document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('loginForm');
  const signupForm = document.getElementById('signupForm');
  const loginLink = document.getElementById('loginLink');
  const signupLink = document.getElementById('signupLink');


  if (loginForm && signupForm && loginLink && signupLink) {
    loginLink.addEventListener('click', function(event) {
      event.preventDefault();
      loginForm.style.display = 'block';
      signupForm.style.display = 'none';
    });

    signupLink.addEventListener('click', function(event) {
      event.preventDefault();
      loginForm.style.display = 'none';
      signupForm.style.display = 'block';
    });
  }
});
const url = '127.0.0.1:8000';

// Assuming you have a form with input fields for username and password
const username = document.getElementById('username').value;
const password = document.getElementById('password').value;
const firstname = document.getElementById('firstname').value;
const lastname = document.getElementById('lastname').value;

const data = {
  user_id: null,
  user_name: username,
  password: password,
  first_name: firstname,
  last_name: lastname,
  registration_date: null,
  last_login_date: null
};
function submit()
{

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    // You may need to include additional headers, such as authorization tokens
  },
  body: JSON.stringify(data)
})
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Success:', data);
    // Handle the successful response from the server
  })
  .catch(error => {
    console.error('Error:', error);
    // Handle errors, such as network issues or server errors
  });


}