% include('template/header.tpl', title='Practica 6', s=menu)
<center><h1>Catalogo</h1></center>
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
<form name="comprar" action="/comprar" method="post" accept-charset="utf-8">
  <ul>
    <li><label for="bookname">Introduce id del libro:</label>
    <input type="text" name="id" placeholder="0"></li>
     <input type="submit" value="comprar">
  </ul>

</form>

% include('template/footer.tpl')
