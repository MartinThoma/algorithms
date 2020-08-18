'use strict';

makePassword();

// http://stackoverflow.com/a/11935263/562769
function getRandomSubarray(arr, size) {
    var shuffled = arr.slice(0), i = arr.length, temp, index;
    while (i--) {
        index = Math.floor(i * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(0, size);
}

/**
 * Creates a password
 * @param {bool} digitFlag Should digits be used?
 * @param {bool} smallLetterFlag Should small letters be used?
 * @param {bool} capitalLettersFlag Should big letters be used?
 * @return {Number} Generated password
 */
function createPassword(digits, digitsFlag, smallLettersFlag, capitalLettersFlag, noConfusableCharsFlag) {
    var elements = new Array();
    if (digitsFlag) {
        elements = ("0123456789".split("")).concat(elements);
    }
    if (smallLettersFlag) {
        if (noConfusableCharsFlag) {

            elements = ("abcdefghikmnpqrstwxyz".split("")).concat(elements);
        } else {
            elements = ("abcdefghijklmnopqrstuvwxyz".split("")).concat(elements);
        }
    }

    if (capitalLettersFlag) {
        if (noConfusableCharsFlag) {
            elements = ("ABCDEFGHIJKLMNPQRSTUVWXYZ".split("")).concat(elements);
        } else {
            elements = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("")).concat(elements);
        }
    }

    return getRandomSubarray(elements, digits).join("");
}

function makePassword() {
    var digits = parseInt(document.getElementById("digits").value);
    var pEl = document.getElementById("password");
    var digitFlag = document.getElementById("digitsFlag").checked;
    var smallLettersFlag = document.getElementById("smallLettersFlag").checked;
    var capitalLettersFlag = document.getElementById("capitalLettersFlag").checked;
    var noConfusableCharsFlag = document.getElementById("noConfusableCharsFlag").checked;
    pEl.value = createPassword(digits, digitFlag, smallLettersFlag, capitalLettersFlag, noConfusableCharsFlag);
}
