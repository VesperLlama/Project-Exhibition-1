new Autocomplete("#autocomplete", {
  search: (input) => {
    const url = `/search_movie/?search=${input}`;

    return new Promise((resolve) => {
      if (input.length < 3) {
        return resolve([]);
      }
      
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          resolve(data.id);
        });
    });
  },
  getResultValue: result => result,
  onSubmit: result => {
    $.ajax({
      type: "GET",
      url: `/movie/?movie=${result}`,
      // data: result,
      // dataType: "string",
    });
  },
});
