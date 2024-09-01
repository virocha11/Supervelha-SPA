// FUNCOES ABRIR E FECHAR MODAL PARA USUARIO CONFIRMAR SE DESEJA SAIR DO SITE

function abrir_modal(carregar_modal){
    console.log("Carregar a janela modal: "+ carregar_modal);
    let modal = document.getElementById(carregar_modal);
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';

}
function fechar_modal(fechar_modal){
    console.log("Fechar a janela modal: "+ fechar_modal);
    let modal = document.getElementById(fechar_modal);

    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}
// FIM FUNCOES ABRIR E FECHAR MODAL

