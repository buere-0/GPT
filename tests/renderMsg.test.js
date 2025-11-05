const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { renderMsg, comparatorSymbol, isTriggered } = require('../src/renderMsg');

describe('comparatorSymbol', () => {
  it('uses strict operators by default', () => {
    assert.equal(comparatorSymbol('above', false), '&gt;');
    assert.equal(comparatorSymbol('below', false), '&lt;');
  });

  it('uses inclusive operators when requested', () => {
    assert.equal(comparatorSymbol('above', true), '&ge;');
    assert.equal(comparatorSymbol('below', true), '&le;');
  });
});

describe('isTriggered', () => {
  it('strict above requires greater than', () => {
    assert.equal(isTriggered(10, 10, 'above', false), false);
    assert.equal(isTriggered(11, 10, 'above', false), true);
  });

  it('inclusive above allows equality', () => {
    assert.equal(isTriggered(10, 10, 'above', true), true);
  });

  it('strict below requires less than', () => {
    assert.equal(isTriggered(10, 10, 'below', false), false);
    assert.equal(isTriggered(9, 10, 'below', false), true);
  });

  it('inclusive below allows equality', () => {
    assert.equal(isTriggered(10, 10, 'below', true), true);
  });
});

describe('renderMsg', () => {
  const baseConfig = {
    price: 100,
    threshold: 100,
    direction: 'above',
    symbol: 'Índice'
  };

  it('strict rule handles ties without triggering', () => {
    const html = renderMsg({ ...baseConfig, rule: 'strict' });
    assert.ok(html.includes('&gt;'));
    assert.ok(html.includes('Sem rompimento'));
  });

  it('inclusive rule handles ties as trigger', () => {
    const html = renderMsg({ ...baseConfig, rule: 'inclusive' });
    assert.ok(html.includes('&ge;'));
    assert.ok(html.includes('Rompimento detectado'));
  });

  it('below direction uses lt entities', () => {
    const html = renderMsg({ ...baseConfig, direction: 'below', price: 90, threshold: 100 });
    assert.ok(html.includes('&lt;'));
    assert.ok(html.includes('Rompimento detectado'));
  });

  it('inclusive below counts ties', () => {
    const html = renderMsg({ ...baseConfig, direction: 'below', rule: 'inclusive' });
    assert.ok(html.includes('&le;'));
    assert.ok(html.includes('Rompimento detectado'));
  });

  it('includes contextual information with safe draw', () => {
    const html = renderMsg({ ...baseConfig, safeDraw: true, source: 'drag', mode: 'manual', isDemo: true });
    assert.ok(html.includes('Modo Manual'));
    assert.ok(html.includes('DEMO'));
    assert.ok(html.includes('Arquivo arrastado'));
    assert.ok(html.includes('Safe draw ativo'));
    assert.ok(html.split('<br>').length > 1);
  });

  it('falls back for unknown options', () => {
    const html = renderMsg({ ...baseConfig, mode: 'unknown', source: '??' });
    assert.ok(html.includes('Modo Automático'));
    assert.ok(html.includes('Arquivo carregado'));
  });

  it('produces html without newlines', () => {
    const html = renderMsg(baseConfig);
    assert.ok(!/\n/.test(html));
  });

  it('requires both price and threshold', () => {
    assert.throws(() => renderMsg({ price: 10 }));
    assert.throws(() => renderMsg({ threshold: 10 }));
  });
});
