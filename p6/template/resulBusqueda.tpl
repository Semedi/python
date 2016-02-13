% include('template/header.tpl', title='Practica 6', s=menu)
<center><h1>Resultados de la Busqueda</h1></center>
%if (len(rows)>0):
	<center><table>
	<tr><th>id</th><th>Titulo</th><th>Autor</th><th>Genero</th></tr>
	%for row in rows:
		<tr>
		%for col in row:
			<td>{{col}}</td>
		%end
		</tr>
		
	%end
	</table></center>
%else: 
	<h2>No se han encontrado resultados<h2>
	<a href="/busqueda">volver a la busqueda</a>
%end

% include('template/footer.tpl')