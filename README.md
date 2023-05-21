# RecipeGenius
Inspiration
Our team created RecipeGenius to solve the problem of not knowing what to cook for a meal when we had limited ingredients in our fridge. We wanted to make it easy for people to find recipes that match their preferences and the ingredients they have on hand.

What it does
Using various coding languages such as CSS, Javascript, Python, and HTML, RecipeGenius is able to scan the photo of the fridge that you send, and using the Google Vision API, we are able to determine which ingredients you have in your fridge. Once we have determined the ingredients, we then ask you what cuisine and meal type you feel like eating. Once we have this information, we pass a prompt to ChatGPT using the GPT API. We then return all details about the recipe including ingredients, the recipe, and nutritional info.

How we built it
To build RecipeGenius we used a combination of several technologies and tools. We primarily used 4 coding languages which were Python, CSS, Javascript, and HTML. We largely used Python Flask for our back-end programming, including the authentication and login system which also used sqlite DB's, and acquiring the GPT response from our API. We used HTML to create the webpage and its functions and then we used CSS to style the website and made it aesthetically pleasing, and we used Javascript to process the front-end information and AJAX to send it to the back-end so that it can be processed. We also used OpenCV and the Google Vision API to find ingredients that are in the fridge and the GPT API to find out which recipe you can make. Additionally, we utilized preprocessing techniques with algorithms like edge detection and color detection to further increase the capability and accuracy of the Vision API.

Challenges we ran into
One of the main challenges we faced was implementing a login system that would securely authenticate users and prevent unauthorized access to the dashboard. We had to do extensive research and testing to ensure that our login system was secure.

Another pressing challenge we faced, especially in the beginning, was the internet. It was really slow and it really halted our progress.

We also faced challenges while working with CSS for the first time. While we had some experience with HTML, CSS was a new technology for us, and we had to spend some time learning how to use it effectively to create a visually appealing and responsive interface for the dashboard.

We struggled with connecting the file we uploaded on the front end to the back end to get the ingredients that were in the picture using AJAX. This was a major roadblock that took a lot of perseverance and effort to overcome. Some of the preprocessing algorithms also required some research to perform.

We also struggled to have effective communication with one of our team members who couldn't be with us due to him being sick. Additionally, adding the navbar was challenging as our CSS caused unforeseen issues and prevented our navbar from displaying correctly for a while.

Accomplishments that we're proud of
Despite facing numerous challenges and struggling with low morale at times, we take pride in persevering through our obstacles. One of our team members battled sickness but still managed to contribute significantly, even while feeling fatigued and unwell. We feel a great sense of accomplishment in having developed a functional website of RecipeGenius that not only gives out amazing recipes but also has a functioning database that can authenticate users securely. Additionally, we used Natural Language Processing techniques to create the perfect prompt for the GPT API to curate a unique recipe each time.

What we learned
We learned a lot about machine learning, artificial intelligence, and the challenges of CSS. We also learned how to integrate different technologies and frameworks to create a web application. We have also become more familiar with Javascript throughout this hackathon. Additionally, we gained valuable experience in developing user interfaces and creating a smooth user experience.

What's next for RecipeGenius
Our team will work further to add on more features past simply creating recipes for our end user, we could begin to accept multiple photos of different places around the kitchen, not just the fridge, in order to create better recipes for the users. Additionally, we hope to diversify the number of cuisines we can give recipes for. We also hope to improve the scalability of the application such that it can become a real brand in the future.
