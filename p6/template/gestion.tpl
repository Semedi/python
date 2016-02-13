% include('template/header.tpl', title='Practica 6', s=menu)
<center><h1>Gestion</h1></center>
%if (len(rows)>0):
	<center><h1>Mis libros</h1></center>
	<center>
	<table>
	<tr><th>id</th><th>Titulo</th><th>Autor</th><th>Genero</th></tr>
	%for row in rows:

		<tr>

		%for col in row:
			<td>{{col}}</td>

		%end
		<p><b>id:{{row[0]}}</b><a href='/doGestion?eliminar=1&id={{row[0]}}'> eliminar</a> <a href="/doGestion?eliminar='0'"> modificar</a> </p>

		</tr>

	%end
	</table>
</center>
%else:
	<h2>Aun no tienes libros en tu lista<h2>
%end
% include('template/footer.tpl')
