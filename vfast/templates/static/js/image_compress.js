
function imageCompress() {
  const files = this.files;
  for (var i = 0; i < files.length; i++) {
    uploadPreview(files[i]);

  }
}

function uploadPreview(file) {
  var reader = window.URL || window.webKitURL;
  const contentType = file.type;
  if (reader && reader.createObjectURL) {
    const image = document.createElement("img"),
      url = reader.createObjectURL(file);

    image.src = url;
    image.onload = function(){
      const data = compress(image)
        // $div = $('<div class="col-md-3"></div>').css("background-image", "url(" + data + ")");
      // $("body").append($div);
      // console.log(data.split(",")[1]);
      // console.log(b64toBlob(data.split(",")[1], contentType));

        var imgBlob = b64toBlob(data.split(",")[1], contentType);
        var form = new FormData();
        form.append("headimg",imgBlob);
        form.append("uid",$("#uid").val());
        $.ajax({
                url:"/u/editpage/change_headimg",
                type:"post",
                data:form,
                processData:false,
                contentType:false,
                dataType:"json",
                success:function(data){
                    $("#uheadimg_this").attr("src",data.headimg);
                    $("#uheadimg").attr("src",data.headimg);
                    showPrompt("头像已更换~");
                },
                error:function(e){
                    console.log(e);
                }
            });

      reader.revokeObjectURL(url);
    };
  }
}

function compress(img) {
  const canvas = document.createElement("canvas");
const ctx = canvas.getContext('2d');
//    瓦片canvas
const tCanvas = document.createElement("canvas");
const tctx = tCanvas.getContext("2d");

  const initSize = img.src.length;

  var width = img.width,
    height = img.height,
    ratio = width * height / 4000000;

  //如果图片大于四百万像素，计算压缩比并将大小压至400万以下
  if (ratio > 1) {
    ratio = Math.sqrt(ratio);
    width /= ratio;
    height /= ratio;
  } else {
    ratio = 1;
  }

  canvas.width = width;
  canvas.height = height;

  //        铺底色
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  //如果图片像素大于100万则使用瓦片绘制
  var count = width * height / 1000000;
  if (count > 1) {
    count = ~~(Math.sqrt(count) + 1); //计算要分成多少块瓦片

    //            计算每块瓦片的宽和高
    var nw = ~~(width / count);
    var nh = ~~(height / count);

    tCanvas.width = nw;
    tCanvas.height = nh;

    for (var i = 0; i < count; i++) {
      for (var j = 0; j < count; j++) {
        tctx.drawImage(img, i * nw * ratio, j * nh * ratio, nw * ratio, nh * ratio, 0, 0, nw, nh);

        ctx.drawImage(tCanvas, i * nw, j * nh, nw, nh);
      }
    }
  } else {
    ctx.drawImage(img, 0, 0, width, height);
  }

  //进行最小压缩
  var ndata = canvas.toDataURL('image/jpeg', 0.1);

  // console.log('压缩前：' + initSize);
  // console.log('压缩后：' + ndata.length);
  // console.log('压缩率：' + ~~(100 * (initSize - ndata.length) / initSize) + "%");

  tCanvas.width = tCanvas.height = canvas.width = canvas.height = 0;

  return ndata;
}

function b64toBlob(b64Data, contentType, sliceSize) {
  contentType = contentType || '';
  sliceSize = sliceSize || 512;

  var byteCharacters = atob(b64Data);
  var byteArrays = [];

  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);

    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);

    byteArrays.push(byteArray);
  }

  try {
    var blob = new Blob(byteArrays, {
      type: contentType
    });

    return blob;
  } catch (e) {
    // TypeError old chrome and FF
    window.BlobBuilder = window.BlobBuilder ||
      window.WebKitBlobBuilder ||
      window.MozBlobBuilder ||
      window.MSBlobBuilder;
    if (e.name == 'TypeError' && window.BlobBuilder) {
      var bb = new BlobBuilder();
      bb.append(byteArrays);
      blob = bb.getBlob(contentType);
      
      return blob;
    } else if (e.name == "InvalidStateError") {
      // InvalidStateError (tested on FF13 WinXP)
      blob = new Blob(byteArrays, {
        type: contentType
      });
      
      return blob;
    } else {
      return;
    }
  }

}