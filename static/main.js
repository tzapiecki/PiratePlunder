
var game = new Phaser.Game(800, 600, Phaser.WEBGL, 'gameDiv');

var mainState = {
    preload: function(){
        
    },

<<<<<<< HEAD
    create: function() {
=======
    game.load.image('sky', 'assets/skies/sky.png');
    game.load.image('dragonTexture', 'assets/creature/dragon.png');
    game.load.json('dragonMesh', 'assets/creature/dragon.json');
>>>>>>> 8a86c301519c9319c49fe4a5b7154a845497af73

    },

    update:function() {

    }
}

game.state.add("mainState", mainState);
game.state.start("mainState");