function medHPop(name, date, description) {
       mhl = document.getElementById('medHistoryListing');
       a = document.createElement('a');
       a.setAttribute('href', "#");
       a.setAttribute('class', 'list-group-item list-group-item-action flex-column align-items-start');
       mhl.prepend(a);
       d = document.createElement('div');
       d.setAttribute('class', 'd-flex w-100 justify-content-between')
       a.append(d);
       h = document.createElement('h5');
       h.setAttribute('class', 'mb-1');
       h.innerText = name;
       d.append(h)
       s = document.createElement('small');
       s.setAttribute('class', 'text-muted');
       s.innerText = date;
       d.append(s);
       s = document.createElement('small');
       s.setAttribute('class', 'text-muted');
       s.innerText = description;
       a.append(s);
}