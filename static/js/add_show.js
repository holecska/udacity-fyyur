
document.getElementById('add_show').onsubmit = function(e) {
  e.preventDefault(); //nem engedi elküldeni a formot, prevent = meggátol
  const artist = document.getElementById('artist_id').value;
  const venue = document.getElementById('venue_id').value;
  const start = document.getElementById('start_time').value;

  fetch('/shows/create', {
    method: 'POST',
    body: JSON.stringify({
      'artist': artist,
      'venue': venue,
      'start': start
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response){
      return response.json();
  })
  .then(function(res){
    if (res['success'] === 'ok') {
        window.location.href = '/';
    }
    else {
      window.location.href = '/';
      window.location.href = '/errors/500.html';
    }
  });
};
