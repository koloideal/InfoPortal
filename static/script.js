document.addEventListener('DOMContentLoaded', function () {
          const flashOk = document.getElementById('success');

          flashOk.addEventListener('animationend', function () {
            flashOk.remove();
          });
        });

document.addEventListener('DOMContentLoaded', function () {
        const flashErr = document.getElementById('bad');

        flashErr.addEventListener('animationend', function () {
          flashErr.remove();
        });
      });
