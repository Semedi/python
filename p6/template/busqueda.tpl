% include('template/header.tpl', title='Practica 6', s=menu)
<center>
	<form name="search" action="/busqueda" method="post" accept-charset="utf-8">
		<h1>Busqueda</h1>
		<input type="text" name="searchterm" placeholder="Introduce tu busqueda" />
		<select name="campo">
			<option value="Titulo">Titulo
			<option value="Autor">Autor
			<option value="Categoria" selected>Categoria
		</select>
		<input type="submit" value="Buscar">
		
	</form>
</center>
 
% include('template/footer.tpl')
 