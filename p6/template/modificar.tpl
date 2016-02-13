% include('template/header.tpl', title='Practica 6', s=menu)

<center><h1>Modificar</h1></center>
<form action="/modificar">
  <fieldset>
    <legend>Datos del libro:</legend>
    Titulo:<br>
    <input type="text" name="titulo" value="">
    <br>
    Autor:<br>
    <input type="text" name="autor" value="">
    <br>
    Genero:<br>
    <input type="text" name="autor" value="">
    <br>
    <input type="submit" value="Submit">
  </fieldset>
  <button type="button" id="mod">Confirmar</button>
</form>

% include('template/footer.tpl')
