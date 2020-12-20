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

document.getElementById('create_venue').onsubmit = function(e) {
  e.preventDefault(); //nem engedi elküldeni a formot, prevent = meggátol
  const name = document.getElementById('name').value;
  const city = document.getElementById('city').value;
  const state = document.getElementById('state').value;
  const phone = document.getElementById('phone').value;
  const address = document.getElementById('address').value;
  const facebook_link = document.getElementById('facebook_link').value;
  const heading = document.querySelector('.form-heading').innerText
  const genres = getSelectedOptions(document.getElementById('genres'));
  const image_link = document.getElementById('image_link').value;
  const website =  document.getElementById('website_link').value;
  let seeking_talent

    if (document.getElementById('seeking_talent_Yes').checked) {
      seeking_talent = true;
    }
    else{
      seeking_talent = false;
    }

  const seeking_description = document.getElementById('seeking_description').value;

  fetch('/venues/create', {
    method: 'POST',
    body: JSON.stringify({
      'name': name,
      'city': city,
      'state': state,
      'phone': phone,
      'address': address,
      'genres': genres,
      'facebook_link': facebook_link,
      'image_link': image_link,
      'seeking_description': seeking_description,
      'seeking_talent': seeking_talent,
      'website': website
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
