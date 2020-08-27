# rec-web-demo
The Web Demo App to use the Recommendation Server for Lenskit.

TMDB API:
1) Search based on the title of the movie, then filter the results based on the year of the movie
https://api.themoviedb.org/3/search/movie?api_key=488b5b045c53046a001bf698ed73831e&query=Jumanji

2) Get the image paths
https://api.themoviedb.org/3/movie/{movieId}/images?api_key=488b5b045c53046a001bf698ed73831e&language=en
Example: https://api.themoviedb.org/3/movie/550/images?api_key=488b5b045c53046a001bf698ed73831e&language=en

3) Choose one and get the image:
https://image.tmdb.org/t/p/original/{image.jpg}
https://image.tmdb.org/t/p/original/clkAGOl8GiPLJ0T2HyrgnBXQmx8.jpg
