
var game = new Phaser.Game(800, 600, Phaser.AUTO, 'gameDiv');

var sky;
var backgroundv;

var mainState = {
    preload: function(){
        this.game.load.image('background', 'assets/dawn-sky-bird-875858.jpg');
    },

    create: function() {
        sky = this.game.add.sprite(0, 0, 800, 600, 'background');
        backgroundv = 2;


    },

    update:function() {

        sky.tilePosition.y += backgroundv;

    }
}

game.state.add("mainState", mainState);
game.state.start("mainState");