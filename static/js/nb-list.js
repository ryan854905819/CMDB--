/**
 * Created by Administrator on 2017/10/11.
 */

/*
自执行函数，只在前端有
(function (arg) {
    alert(arg)
})(666)

*/

(function (jq) {

    var requestUrl = "";

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s,i) {
            return args[i];
        });
    };

    /*
    像后台获取数据
     */
    function init() {
        $('#loading').removeClass('hide');

        $.ajax({
            url:requestUrl,
            type: 'GET',
            data: {},
            dataType: 'JSON',
            success:function (response) {
                /* 处理表头 */
                initTableHead(response.table_config);
                initTableBody(response.data_list,response.table_config);
                $('#loading').addClass('hide');
            },
            error:function () {
                $('#loading').addClass('hide');
            }
        })


    }

    function initTableHead(table_config) {
        /*
         table_config = [
                {
                    'q': 'hostname',
                    'title': '主机名',
                },
                {
                    'q': 'sn',
                    'title': '序列号',
                },
                {
                    'q': 'os_platform',
                    'title': '系统',
                },
            ]
         */
        //清除表格行，不然页面没有从新加载，在请求一次字段重复出现
        $('#tHead tr').empty();
            $.each(table_config,function (k,conf) {
                if(conf.display) {
                    var th = document.createElement('th');
                    th.innerHTML = conf.title;
                    $('#tHead tr').append(th);
                }
            });
    }

    function initTableBody(data_list,table_config) {
        /*
        [
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        ]

        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>

         */

        $.each(data_list,function (k,row_dict) {
            // {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},   //row_dict
            // {'hostname':'xx1', 'sn':'xx2', 'os_platform':'xxx2'},

            var tr = document.createElement('tr');
            /*
            table_config
            {
            'q': None,
            'title': '选择',
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
            */
            $.each(table_config,function (kk,vv) {

                if (vv.display) {
                        var td = document.createElement('td');
                        // td.innerHTML = row_dict[vv.q];   //vv.q // None,hostname,sn,os_platform
                        var format_dict = {};
                        $.each(vv.text.kwargs, function (kkk, vvv) {
                            if (vvv[0] == "@") {
                                var name = vvv.substring(1, vvv.length);
                                format_dict[kkk] = row_dict[name];
                            } else {
                                format_dict[kkk] = vvv;
                            }

                        });


                        td.innerHTML = vv.text.tpl.format(format_dict);

                        $(tr).append(td);
                }
            });

            $('#tBody').append(tr);

        })

    }

    jq.extend({
        "nBList":function (url) {
            requestUrl = url;
            init();
        }
    });

})(jQuery);




