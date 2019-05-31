'use strict';

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');
var userId = parseInt(document.getElementById('userId').textContent)
console.log(userId)
var initListeners = () => allCards.forEach(function (el) {
  var hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
    tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    el.classList.remove('moving');
    tinderContainer.classList.remove('tinder_love');
    tinderContainer.classList.remove('tinder_nope');

    var moveOutWidth = document.body.clientWidth;

    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;
    console.log(moveOutWidth - Math.abs(event.deltaX))
    // if (moveOutWidth - Math.abs(event.deltaX) < 1000) {
    //   keep = false;
    // }
    event.target.classList.toggle('removed', !keep);
    if (keep) {
      event.target.style.transform = '';
    } else {
      var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      if (toX > 0) {

        console.log(el.innerHTML)
      } else {
        console.error(el.innerHTML)
      }
	getNextProfile()
      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';

    }
  });
});

const myId = 2;

const swipeLeft = () => {
  console.log("Swiped left");
}

const swipeRight = () => {
  console.log("swiped right");

}

function initCards(card, index) {
  var newCards = document.querySelectorAll('.tinder--card:not(.removed)');
  // console.log(newCards)
  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  allCards = document.querySelectorAll('.tinder--card:not(.removed)');
  // initListeners()
  tinderContainer.classList.add('loaded');
}

// initCards();


// initListeners();

function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love) {
      console.log(card.innerHTML)
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
    } else {
      console.error(card.innerHTML)
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
    }
	   getNextProfile()
    //initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);


let activeProfileId = -1;
function getNextProfile () {
document.getElementById('cardRoot').insertAdjacentHTML('beforeend', `<div class="spinner" id="spinner"></div>`)
  fetch('./api/getNextProfile')
  .then(function(response) {
    console.log('hello')
    return response.json();
  })
  .then(function(myJson) {
    // console.log(JSON.stringify(myJson));
    // console.log(myJson.id)
    activeProfileId = myJson.id;
    // console.log(activeProfileId)
    var spinner = document.getElementById('spinner');
    spinner.remove()
    document.getElementById('cardRoot').insertAdjacentHTML('beforeend', `
   <div class="tinder--card">
      <div class="thumb">
        <img src="./file/pictures/${myJson.email.replace('@', '-').replace('.', '-')}.jpeg" style="width:200;height:200;"}>
      </div>
      <h3 class="name">${myJson.name}</h3>
      <p>${myJson.status}</p>
      <p>Looking for: ${myJson.lookingFor}</p>
      <div class="left info">
        <p><strong>Skills</strong></p>
        ${generatePList(myJson.skills)}
      </div>
      <div class="right info">
        <p><strong>Interested In</strong></p>
        ${generatePList(myJson.interests)}
      </div>
      <div class="description">
        <p>${myJson.description}</p>
      </div>
      <div class="socials">
        ${generateSocials(myJson.socials)}
      </div>
    </div>`)
   allCards = document.querySelectorAll('.tinder--card');
   initListeners()
  initCards();
});
}

function generatePList (arr) {
  let html = ''
  arr.forEach(el => {
    html += `<p>-${el}</p>`
  })
  return html
}

function generateSocials (socials) {
  let html = ''
  if (socials.facebook) {
    html += `<a href="${socials.facebook}"><i class="fa fa-facebook"></i></a>`
  }
   if (socials.linkedin) {
    html += `<a href="${socials.facebook}"><i class="fa fa-linkedin"></i></a>`
  }
   if (socials.twitter) {
    html += `<a href="${socials.facebook}"><i class="fa fa-twitter"></i></a>`
  }
  return html
}

document.getElementById('message').addEventListener('click', () => {
  window.location.href = "./messages";
})

getNextProfile()
nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);
