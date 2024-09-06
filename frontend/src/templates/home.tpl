{{ define "home" }}
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8" />
  <title>Leadopt</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous" />
  <link rel="stylesheet" href="/static/style.css" type="text/css" />
  <link rel="icon" href="/static/favicon.png" type="image/x-icon" />
  <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" />
</head>

<body>
  <div class="header">
    <div class="container">
      <h1>
        <a href="/"> Lead Optimizer for LinkedIn Profile </a>
      </h1>
      <!--<a href="#" class="text-muted">View on GitHub</a>-->
    </div>
  </div>

  <div class="container posts mt-0">
    <form class="form-inline" method="POST" action="/post">
      <label class="sr-only" for="name">First Name</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">First Name</div>
        </div>
        <input type="text" class="form-control" id="first_name" name="first_name" required />
      </div>


      <label class="sr-only" for="name">Last Name</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Last Name</div>
        </div>
        <input type="text" class="form-control" id="last_name" name="last_name" required />
      </div>



      <label class="sr-only" for="name">Company Name</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Company Name</div>
        </div>
        <input type="text" class="form-control" id="company" name="company" required />
      </div>


      <label class="sr-only" for="name">Position</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Position</div>
        </div>
        <input type="text" class="form-control" id="position" name="position" required />
      </div>


      <label class="sr-only" for="name">Connections</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Connections</div>
        </div>
        <input type="text" class="form-control" id="connections" name="connections" required />
      </div>

      <label class="sr-only" for="name">Connection Dist</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Connection Dist</div>
        </div>
        <input type="text" class="form-control" id="connection_dist" name="connection_dist" required />
      </div>

      <label class="sr-only" for="name">Linkedin URL</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Linkedin URL</div>
        </div>
        <input type="text" class="form-control" id="linkedin_url" name="linkedin_url" required />
      </div>


      <label class="sr-only" for="message">Activities</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Activities</div>
        </div>
        <input type="text" class="form-control" id="activity" name="activity" required />
      </div>
      <button type="submit" class="btn btn-primary mb-2">
        Save Profile
      </button>
    </form>

    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Avatar</th>
          <th scope="col">Full Name</th>
          <th scope="col">Connections</th>
          <th scope="col">Connection Dist</th>
          <th scope="col">LinkedIn URL</th>
          <th scope="col">Created At</th>
          <th scope="col">Activity</th>
        </tr>
      </thead>
      <tbody>
        {{ range $index, $profile:= .profiles }}
        <tr>
          <th scope="row">{{add $index 1}}</th>
          <td><img src="{{$profile.Avatar}}" alt="{{$profile.Avatar}}" /></td>
          <td>{{$profile.FirstName}} {{$profile.LastName}}</td>
          <td>{{ $profile.Connections }}</td>
          <td>{{ $profile.ConnectionDist }}</td>
          <td>{{ $profile.LinkedInURL }}</td>
          <td>{{ $profile.CreatedAt | since }} ago</td>
          <td>{{ $profile.Activity }} </td>
        </tr>
        {{ else }}
        <div class="alert alert-info" role="alert">
          No profiles are logged to the Leadopt yet.
        </div>
        {{ end }}
      </tbody>
    </table>
</body>

</html>
{{ end }}