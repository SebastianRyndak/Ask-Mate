function markAnswer() {
    if (confirm('Mark this answer as resolve?')) {
        alert('Answer marked');
    } else {
        alert('Action canceled');
    }
}

function unmarkAnswer() {
    if (confirm('Unmark this answer as resolve?')) {
        alert('Answer unmarked');
    } else {
        alert('Action canceled');
    }
}

window.addEventListener('scroll',function() {
    //When scroll change, you save it on localStorage.
    localStorage.setItem('scrollPosition',window.scrollY);
},false);

window.addEventListener('load',function() {
    if(localStorage.getItem('scrollPosition') !== null)
       window.scrollTo(0, localStorage.getItem('scrollPosition'));
},false);