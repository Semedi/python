% include('template/header.tpl', title='Practica 6', s=menu)
<center><h1>Registro</h1></center>
<section class="loginform">
  <form name="login" action="/registro" method="post" accept-charset="utf-8">
    <ul>
      <li><label for="usermail">Email</label>
      <input type="email" name="user" placeholder="yourname@email.com" required></li>
      <li><label for="password">Password</label>
      <input type="password" name="password" placeholder="password" required></li>
      <li> <input type="submit" value="Registrar"> </li>
    </ul>

  </form>
</section>

% include('template/footer.tpl')
