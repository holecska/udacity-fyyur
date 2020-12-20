// CREATE NEW ARTIST!!!
function getSelectedOptions(sel) {
  var opts = [],
    opt;
  // loop through options in select list
  for (var i = 0, len = sel.options.length; i < len; i++) {
    opt = sel.options[i];
    // check if selected
    if (opt.selected) {
      // add to array of option elements to return from this function
      opts.push(opt.value);
    }
  }
  // return array containing references to selected option elements
  return opts;
}

document.getElementById('create_artist').onsubmit = function(e) {
  e.preventDefault(); //nem engedi elküldeni a formot, prevent = meggátol
  const name = document.getElementById('name').value;
  const city = document.getElementById('city').value;
  const state = document.getElementById('state').value;
  const phone = document.getElementById('phone').value;
  const image_link = document.getElementById('image_link').value;
  const website =  document.getElementById('website').value;
  const facebook_link = document.getElementById('facebook_link').value;

  const seeking_description = document.getElementById('seeking_description').value;
  const genres = getSelectedOptions(document.getElementById('genres'));

  let seeking_venue

    if (document.getElementById('seeking_venue_Yes').checked) {
      seeking_venue = true;
    }
    else{
      seeking_venue = false;
    }

  fetch('/artists/create', {
    method: 'POST',
    body: JSON.stringify({
      'name': name,
      'city': city,
      'state': state,
      'phone': phone,
      'genres': genres,
      'facebook_link': facebook_link,
      'image_link': image_link,
      'website': website,
      'seeking_description': seeking_description,
      'seeking_venue': seeking_venue
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
