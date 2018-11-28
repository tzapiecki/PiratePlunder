
// Initialize the Phaser Game object and set default game window size
var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 200 }
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var game = new Phaser.Game(config);
var background;

function preload () {
    // Load & Define our game assets
    this.load.setBaseURL("{{ url_for('static', filename='assets') }}");
    this.load.image('background', "assets/bg.png");
    this.load.image('ship',"ship.png")
};


function create () {
    background=this.add.tileSprite(0, 0,1600,1170, 'background');
    this.add.sprite(350,90,'ship').setScale(0.55);
};

function update () {
  background.x +=2;
};