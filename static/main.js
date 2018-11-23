
var game = new Phaser.Game(800, 600, Phaser.WEBGL, 'gameDiv');

var mainState = {
    preload: function(){
        
    },

    create: function() {

    },

    update:function() {

    }
}

game.state.add("mainState", mainState);
game.state.start("mainState");