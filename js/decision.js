(function(root){
  function decideSide(topY, botY, lastY, buffer, boundaryMode = 'strict'){
    const inclusive = boundaryMode === 'inclusive';
    const topThreshold = topY - buffer;
    const bottomThreshold = botY + buffer;

    if(inclusive){
      if(lastY <= topThreshold) return 'COMPRA';
      if(lastY >= bottomThreshold) return 'VENDA';
      return 'ESPERA';
    }

    if(lastY < topThreshold) return 'COMPRA';
    if(lastY > bottomThreshold) return 'VENDA';
    return 'ESPERA';
  }

  const api = { decideSide };
  if(typeof module !== 'undefined' && module.exports){
    module.exports = api;
  }
  root.decideSide = decideSide;
})(typeof window !== 'undefined' ? window : globalThis);
