const MODE_LABEL = {
  auto: 'Modo Automático',
  manual: 'Modo Manual'
};

const SOURCE_LABEL = {
  upload: 'Arquivo carregado',
  drag: 'Arquivo arrastado',
  paste: 'Conteúdo colado'
};

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function comparatorSymbol(direction, inclusive) {
  if (direction === 'below') {
    return inclusive ? '&le;' : '&lt;';
  }
  return inclusive ? '&ge;' : '&gt;';
}

function normalizeMode(mode) {
  return MODE_LABEL[mode] ? mode : 'auto';
}

function normalizeSource(source) {
  return SOURCE_LABEL[source] ? source : 'upload';
}

function formatNumber(value, decimals) {
  const formatter = new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
  return formatter.format(value);
}

function isTriggered(price, threshold, direction, inclusive) {
  if (direction === 'below') {
    return inclusive ? price <= threshold : price < threshold;
  }
  return inclusive ? price >= threshold : price > threshold;
}

function renderMsg(options = {}) {
  const {
    mode = 'auto',
    isDemo = false,
    source = 'upload',
    safeDraw = false,
    rule = 'strict',
    direction = 'above',
    threshold,
    price,
    symbol = 'Preço',
    decimals = 2
  } = options;

  if (price === undefined || threshold === undefined) {
    throw new Error('renderMsg requires both price and threshold values.');
  }

  const normalizedMode = normalizeMode(mode);
  const normalizedSource = normalizeSource(source);
  const inclusive = rule === 'inclusive';

  const lines = [];

  const title = [escapeHtml(MODE_LABEL[normalizedMode])];
  if (isDemo) {
    title.push('<span class="tag">DEMO</span>');
  }
  lines.push(`<strong>${title.join(' ')}</strong>`);

  const context = [escapeHtml(SOURCE_LABEL[normalizedSource])];
  if (safeDraw) {
    context.push('Safe draw ativo');
  }
  lines.push(context.join(' • '));

  const symbolLabel = escapeHtml(symbol);
  const formattedPrice = escapeHtml(formatNumber(price, decimals));
  const formattedThreshold = escapeHtml(formatNumber(threshold, decimals));
  const comparator = comparatorSymbol(direction, inclusive);

  lines.push(`${symbolLabel} ${formattedPrice} ${comparator} Limite ${formattedThreshold}`);

  const triggered = isTriggered(price, threshold, direction, inclusive);
  lines.push(triggered ? '<span class="ok">Rompimento detectado</span>' : '<span class="warn">Sem rompimento</span>');

  return lines.join('<br>');
}

module.exports = {
  renderMsg,
  comparatorSymbol,
  isTriggered
};
