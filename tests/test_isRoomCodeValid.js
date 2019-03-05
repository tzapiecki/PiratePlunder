const inputTests = [
    'hello',
    ',,,,',
    'hello,',
    'AaAa',
    'AAAA'
]


/* 
 * isRoomCodeValid verifies that the user entered code does not contain not accepted characters.
 * @param code: a String of the user entered code
 * @returns a boolean -> true if valid, false if not valid
 */
function isRoomCodeValid (code) {
    if(/^[a-zA-Z0-9]+$/.test(code)) return true;
    else return false;
}


function testIsRoomCodeValid() {
    if (isRoomCodeValid(inputTests[0]) == false) return inputTests[0];
    if (isRoomCodeValid(inputTests[1]) == true) return inputTests[1];
    if (isRoomCodeValid(inputTests[2]) == true) return inputTests[2];
    if (isRoomCodeValid(inputTests[3]) == false) return inputTests[3];
    if (isRoomCodeValid(inputTests[4]) == false) return inputTests[4];

    return 'Success'
}



let response = testIsRoomCodeValid();
if (response == 'Success') console.log('All tests passed');
else console.log('This input failed: ', response);