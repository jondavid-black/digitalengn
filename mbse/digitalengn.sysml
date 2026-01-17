package digitalengn {
    part digitalengn {
        part digitalengn_web;
        part docsengn_web;
        part engn_cli;

        part persistent_components {
            part gitlab;
            part openproject;
            part gitlab_runner;
        }

        part dynamic_components {
            part vscode;
            part penpot;
            part docsengn_dynamic;
        }
    }
}
