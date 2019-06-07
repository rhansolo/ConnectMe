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
        swipeRight();
        // console.log(el.innerHTML)
      } else {
        swipeLeft();
        // console.error(el.innerHTML)
      }
      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';

    }
  });
});

const myId = 2;

const swipeLeft = () => {
  const url = `./left?user1=${userId}&user2=${activeProfileId}`
  // console.error(url)
   fetch(url)
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(myJson)
      getNextProfile();
  })
}

// const matchText = document.getElementById('matchText')
// matchText.style.display = 'none';

const showMatch = () => {
  matchText.style.display = 'block';
  setTimeout(() => {matchText.style.display = 'none';}, 500);
}

// const noMoreSwipeText = document.getElementById('noMoreSwipeText')
// noMoreSwipeText.style.display = 'none'

const swipeRight = () => {
  const url = `./right?user1=${userId}&user2=${activeProfileId}`
  fetch(url)
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(myJson)
    const match = myJson.some(arr => {
      return arr[1] == activeProfileId && arr[2] == userId
    })
    if (match) {
      addMatchText()
    } else {
      getNextProfile();
    }
  })
}

const texty = document.getElementById('texty')
const addMatchText = () => {
  texty.innerHTML = ` <div class="centered" id="matchText">
  <h1>It's a match!</h1>
  <button class="form-control btn my-2 my-sm-0 smally" id="sendMessage">Send a message</button>
  <button class="form-control btn my-2 my-sm-0 smally" id="ok">Ok</button>
  </div>`

  document.getElementById('sendMessage').addEventListener('click', () => {
    window.location = `../message/${activeProfileId}`
  })

  document.getElementById('ok').addEventListener('click', () => {
    removeMatchText();
    getNextProfile();
  })
}

const removeMatchText = () => {
  const elem = document.getElementById('matchText')
  elem.parentNode.removeChild(elem)
}

const addNoMoreSwipeText = () => {
  texty.innerHTML = `<div class="centered" id="noMoreSwipeText"><br><h1 style="text-align:center;">There are no more users for you to swipe on.</h1><br><h1 style="text-align:center;">Check back later!</h1></div>`
}

const removeNoMoreSwipeText = () => {
  const elem = document.getElementById('noMoreSwipeText')
  elem.parentNode.removeChild(elem)
}


// addMatchText();

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
      // console.log(card.innerHTML)
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      swipeRight()
    } else {
      // console.error(card.innerHTML)
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
      swipeLeft()
    }
	   // getNextProfile()
    //initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);


let activeProfileId = -1;
function getNextProfile () {
document.getElementById('cardRoot').insertAdjacentHTML('beforeend', `<div class="spinner" id="spinner"></div>`)
  fetch(`./api/${userId}/getNextProfile`)
  .then(function(response) {
    console.log(response)
    return response.json();
  })
  .then(function(myJson) {
    var spinner = document.getElementById('spinner');
    spinner.remove()
    if (!myJson) {
      addNoMoreSwipeText();
    } else {
       activeProfileId = myJson.id;
        let imageUrl = "./file/pictures/default.jpeg"
        fetch(`./file/pictures/${myJson.email.replace('@', '-').replace('.', '-')}.jpeg`)
        .then((response) => {
          if (response.status !== 404) {
            imageUrl = `./file/pictures/${myJson.email.replace('@', '-').replace('.', '-')}.jpeg`
          }

          document.getElementById('cardRoot').insertAdjacentHTML('beforeend', `
         <div class="tinder--card">
            <div class="thumb info">
              <img src="${imageUrl}" style="width:200;height:200;"}>
            </div>
            <h3 class="name interested">${myJson.name}</h3>
            <p>${myJson.status}</p>
            <hr>
            <p>Major: ${myJson.skills[0]}</p>
            <hr>
            <div class="info">
              <p class="interested"><strong>Interested In</strong></p>
              ${generatePList(myJson.interests)}
            </div>
            <hr>
            <div class="description">
              <p class="interested"><b>About</b></p>
              <p>${myJson.description}</p>
            </div>
            <hr>
          </div>`)
         allCards = document.querySelectorAll('.tinder--card');
         initListeners()
        initCards();
          })
    }

});
}

function generatePList (arr) {
  let html = ''
  arr.forEach(el => {
    html += `<li>${el}</li>`
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

getNextProfile()
nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);
