const test = require('node:test');
const assert = require('node:assert/strict');

const { decideSide } = require('../js/decision.js');

test('strict mode: breakout and breakdown', () => {
  assert.equal(decideSide(200, 600, 180, 10, 'strict'), 'COMPRA');
  assert.equal(decideSide(200, 600, 620, 10, 'strict'), 'VENDA');
});

test('strict mode: inside range and equality edge cases', () => {
  assert.equal(decideSide(200, 600, 400, 10, 'strict'), 'ESPERA');
  assert.equal(decideSide(200, 600, 190, 10, 'strict'), 'ESPERA');
  assert.equal(decideSide(200, 600, 610, 10, 'strict'), 'ESPERA');
});

test('inclusive mode: equality counts as breakout', () => {
  assert.equal(decideSide(200, 600, 190, 10, 'inclusive'), 'COMPRA');
  assert.equal(decideSide(200, 600, 610, 10, 'inclusive'), 'VENDA');
});

test('buffer adjustments', () => {
  assert.equal(decideSide(200, 600, 191, -5, 'strict'), 'COMPRA');
  assert.equal(decideSide(200, 600, 610, 20, 'strict'), 'ESPERA');
});
