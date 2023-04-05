    /* global instantsearch algoliasearch */

    // Basic auth with username/password is not supported - bug: see https://github.com/searchkit/searchkit/issues/1235
    var globalSearchTerm = '';
    const sk = new Searchkit({
        connection: {
          host: "http://localhost:8000/api/v1/searchkit", // TODO remove hardcoding for deployment
        },
        search_settings: {
          highlight_attributes: ["section_name", "drug_label_product_name", "drug_label_generic_name"],
          snippet_attributes: ["section_text"],
          search_attributes: ["drug_label_product_name", "section_name", "section_text", "drug_label_generic_name"],
          result_attributes: ["id", "label_product_id", "section_name", "section_text", "drug_label_product_name", "drug_label_generic_name", "drug_label_source", "drug_label_link", "drug_label_version_date", "drug_label_product_number", "drug_label_id"],
          facet_attributes: [
            {
              field: "drug_label_source.keyword",
              type: "string",
              attribute: "drug_label_source",
            }, {
                field: "section_name.keyword",
                type: "string",
                attribute: "section_name",
            }, {
                field: "drug_label_product_name.keyword",
                type: "string",
                attribute: "drug_label_product_name",
            }, {
                field: "drug_label_generic_name.keyword",
                type: "string",
                attribute: "drug_label_generic_name",
            }
          ],
        }
      })
  
      const search = instantsearch({
        indexName: "productsection",
        searchClient: SearchkitInstantsearchClient(sk),
        routing: true,
      });
  
      search.addWidgets([
          instantsearch.widgets.searchBox({
              queryHook(query, search) {
                  globalSearchTerm = query;
                  search(query);
              },
              container: "#searchbox",
          }),
          instantsearch.widgets.currentRefinements({
              container: "#current-refinements"
          }),
          instantsearch.widgets.menuSelect({
              container: "#section-name-filter",
              attribute: "section_name",
              field: "section_name.keyword",
              limit: 100
          }),
          instantsearch.widgets.refinementList({
              container: "#drug-label-source-filter",
              attribute: "drug_label_source",
              field: "drug_label_source.keyword",
          }),
          instantsearch.widgets.menuSelect({
              container: "#drug-label-product-name-filter",
              attribute: "drug_label_product_name",
              field: "drug_label_product_name.keyword",
              limit: 100
          }),
          instantsearch.widgets.menuSelect({
              container: "#drug-label-generic-name-filter",
              attribute: "drug_label_generic_name",
              field: "drug_label_generic_name.keyword",
              limit: 100
          }),
          instantsearch.widgets.hits({
              container: "#hits",
              templates: {
                  item(hit, { html, components }) {
                      var singleItemUrl = '';
                      if (globalSearchTerm == '') {
                        // no search term, no highlighting or we will error
                        singleItemUrl = `../data/single_label_view/${hit.drug_label_id}`;
                      } else {
                        singleItemUrl = `../data/single_label_view/${hit.drug_label_id}, ${globalSearchTerm}`;
                      }
                      return html`
                      <a href="${singleItemUrl}">${components.Highlight({ attribute: 'drug_label_product_name', hit })}</a> <br />
                      ${components.Highlight({ attribute: 'drug_label_generic_name', hit })}<br />
                      ${components.Highlight({ attribute: 'section_name', hit })} <br />
                      Source: ${hit.drug_label_source}<br />
                      Version Date: ${hit.drug_label_version_date}<br />
                      Product Number: ${hit.drug_label_product_number}<br />
                      Link: <a href="${hit.drug_label_link}">${hit.drug_label_link}</a><br />
                      <p>${components.Snippet({ attribute: 'section_text', hit })}</p>
                      `;
                  }
              }
          }),
          instantsearch.widgets.pagination({
              container: "#pagination"
          }),
          instantsearch.widgets.hitsPerPage({
              container: '#hits-per-page',
              items: [
                  { label: '10 hits per page', value: 10, default: true },
                  { label: '20 hits per page', value: 20 },
                  { label: '50 hits per page', value: 50 }
              ],
          })
      ]);
  
      search.start();