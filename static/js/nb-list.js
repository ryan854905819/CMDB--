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
    var GLOBAL_CHOICES_DICT = {
        // 'status_choices': [[0,'xxx'],]
        // 'xxxx_choices': [[0,'xxx'],]
    };

    function getChoiceNameByid(choice_name,id) {
        var val;
        var status_choices_list = GLOBAL_CHOICES_DICT[choice_name];
        $.each(status_choices_list,function (kkkk,vvvv) {
            if(id == vvvv[0]){
                val = vvvv[1];
            }
        });
        return val;
    }

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
                /* 处理choice */
                /*
                'global_choices_dict':{
            'status_choices':models.Server.server_status_choices
        }
                 */

                GLOBAL_CHOICES_DICT = response.global_choices_dict;


                /* 处理表头 */
                initTableHead(response.table_config);
                /* 处理数据 */
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

        /*
        //conf 等于下面一个字典，k是列表的一个索引
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
         */


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
        //data_list  下面数据
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
            // {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},   //row_dict取到data_list里面每个字典，k是一个索引
            // {'hostname':'xx1', 'sn':'xx2', 'os_platform':'xxx2'},

            var tr = document.createElement('tr');
            /*

            //vv就是下面这个字典,kk是索引
            table_config
            {
            'q': None,
            'title': '选择',
             'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
            'attr':{'k':'v','edit':'true','od':'@id'},
        },
            */

            $.each(table_config,function (kk,vv) {
                var td = document.createElement('td');
                var format_dict = {};  //用来存放text格式化好的数据
                $.each(vv.attr,function (akk,avv) {
                    if(avv[0] == "@") {
                        var name = avv.substring(1,avv.length);
                         avv= row_dict[name];
                    }
                    td.setAttribute(akk,avv);
                });
                if (vv.display) {
                        // var td = document.createElement('td');
                        // td.innerHTML = row_dict[vv.q];   //vv.q // None,hostname,sn,os_platform
                        // var format_dict = {};  //用来存放格式化好的数据
                        //vv.text.kwargs    就是这种字典{'nid': '@id'} ，kkk那的字典key，vvv拿字典的值
                        $.each(vv.text.kwargs, function (kkk, vvv) {
                            if(vvv.substring(0,2) == "@@"){
                                var name = vvv.substring(2,vvv.length); // status_choices
                                var val = getChoiceNameByid(name,row_dict[vv.q]);
                                format_dict[kkk] = val
                            }
                            else if (vvv[0] == "@") {
                                var name = vvv.substring(1, vvv.length);

                                //{'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},   //row_dict取到data_list里面每个字典，k是一个索引
                                //把{xxx}里面内容替换完成后加format_dict到字典里面去，row_dict[name]拿到是数据库取到的值
                                format_dict[kkk] = row_dict[name];
                            } else {
                                format_dict[kkk] = vvv;
                            }

                        });

                        //字符串进行格式化，把里面{xxx}占位符全部替换成出来，并且赋值给td标签
                        td.innerHTML = vv.text.tpl.format(format_dict);
                        $(tr).append(td);
                }
            });

            $('#tBody').append(tr);

        });

    }

    jq.extend({
        "nBList":function (url) {
            requestUrl = url;
            init();
        }
    });

})(jQuery);




