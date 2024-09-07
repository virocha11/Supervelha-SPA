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

//DEFININDO ROLAGEM DO SCROLL PARA APLICAR A FUNCAO DE VOLTAR AO TOPO DA PAGINA
window.addEventListener('scroll', function(){
    let scroll = document.querySelector('.rolar_cima')
    scroll.classList.toggle('active', window.scrollY > 300)
})

//FUNCAO DE VOLTAR AO TOPO DA PAGINA
function voltar_cima(){
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
}


//HABILITANDO E DESABILITANDO OS CAMPOS DE TROCAS SENHA QUE ESTAO NO PERFIL DO USUARIO
//PARA EVITAR ERROS AO ENVIAR O FORMULARIO SEM TROCAR A SENHA

document.getElementById('trocar_senha').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o comportamento padrão do link

    var senha = document.getElementById('senha');
    if (senha.classList.contains('inativo')) {
        senha.classList.remove('inativo');
        senha.classList.add('ativo');
        senha.disabled = false;
    } else {
        senha.classList.remove('ativo');
        senha.classList.add('inativo');
        senha.disabled = true;
    }    
    senha = document.getElementById('nova_senha');
    if (senha.classList.contains('inativo')) {
        senha.classList.remove('inativo');
        senha.classList.add('ativo');
        senha.disabled = false;
    } else {
        senha.classList.remove('ativo');
        senha.classList.add('inativo');
        senha.disabled = true;
    }    
    senha = document.getElementById('confirma_senha');
    if (senha.classList.contains('inativo')) {
        senha.classList.remove('inativo');
        senha.classList.add('ativo');
        senha.disabled = false;
    } else {
        senha.classList.remove('ativo');
        senha.classList.add('inativo');
        senha.disabled = true;
    }
});
