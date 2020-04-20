function medHPop(id, name, date, description) {
       mhl = document.getElementById('medHistoryListing');
       a = document.createElement('a');
       a.setAttribute('class', 'list-group-item list-group-item-action flex-column align-items-start');
       mhl.prepend(a);
       d = document.createElement('div');
       d.setAttribute('class', 'd-flex w-100 justify-content-between')
       a.append(d);
       h = document.createElement('h5');
       h.setAttribute('class', 'mb-1');
       h.innerText = name;
       d.append(h)
       b = document.createElement('button');
       b.setAttribute('type', 'submit');
       b.setAttribute('class', 'btn btn-outline-danger');
       b.setAttribute('name', 'deleteButton');
       b.setAttribute('value', id);
       b.setAttribute('form', 'medHListing');
       b.innerText = "X"
       d.append(b)
       p = document.createElement('p');
       p.setAttribute('class', 'mb-1');
       p.innerText = description
       a.append(p);
       s = document.createElement('small');
       s.setAttribute('class', 'text-muted');
       s.innerText = date;
       a.append(s);
}